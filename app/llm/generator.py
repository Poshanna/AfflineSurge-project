import os
import json
from dotenv import load_dotenv
from app.services.hash_service import generate_content_hash
from app.models.models import GenerationReference, Selection
from app.database.database import SessionLocal
from app.services.selection_service import get_selection_nodes
from typing import Optional

load_dotenv()

try:
    from pymongo import MongoClient
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    OPENAI_AVAILABLE = False

GENERATED_DIR = "generated_artifacts"
if not os.path.exists(GENERATED_DIR):
    os.makedirs(GENERATED_DIR)


def build_prompt(nodes, artifact_type: str) -> str:
    combined_content = ""
    for node in nodes:
        combined_content += f"## {node.heading}\n{node.body}\n\n"

    prompts = {
        "test_cases": f"""Based on the following document content, generate comprehensive test cases:

{combined_content}

Please format the test cases with Test Case ID, Description, Preconditions, Steps, Expected Results.""",
        "requirements": f"""Based on the following document content, extract and list all requirements:

{combined_content}

Please format each requirement with a unique ID and description.""",
        "traceability_matrix": f"""Based on the following document content, create a traceability matrix:

{combined_content}

Please include requirement IDs, related sections, and test case mapping (if applicable)."""
    }

    return prompts.get(artifact_type, f"Process the following content:\n\n{combined_content}")


def call_llm(prompt: str) -> str:
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    elif OPENAI_AVAILABLE and OPENAI_API_KEY:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    else:
        return "LLM not configured. Please set GEMINI_API_KEY or OPENAI_API_KEY in environment variables."


def compute_source_hash(nodes) -> str:
    all_hashes = []
    for node in sorted(nodes, key=lambda x: x.id):
        all_hashes.append(node.content_hash)
    return generate_content_hash("".join(all_hashes))


def store_artifact(selection_id: int, artifact_type: str, content: str, source_hash: str):
    db = SessionLocal()
    try:
        mongo_id = None
        json_path = None

        if MONGO_AVAILABLE and os.getenv("MONGO_URI"):
            client = MongoClient(os.getenv("MONGO_URI"))
            db_mongo = client["tri9t"]
            collection = db_mongo["artifacts"]
            result = collection.insert_one({
                "selection_id": selection_id,
                "artifact_type": artifact_type,
                "generated_content": content,
                "source_hash": source_hash,
                "created_at": None
            })
            mongo_id = str(result.inserted_id)
        else:
            json_path = os.path.join(GENERATED_DIR, f"artifact_{selection_id}_{artifact_type}_{source_hash[:8]}.json")
            with open(json_path, "w") as f:
                json.dump({
                    "selection_id": selection_id,
                    "artifact_type": artifact_type,
                    "generated_content": content,
                    "source_hash": source_hash
                }, f)

        gen_ref = GenerationReference(
            selection_id=selection_id,
            artifact_type=artifact_type,
            mongo_document_id=mongo_id,
            json_file_path=json_path,
            source_hash=source_hash
        )
        db.add(gen_ref)
        db.commit()
        db.refresh(gen_ref)

        return gen_ref
    finally:
        db.close()


def retrieve_artifact(generation_id: int) -> Optional[dict]:
    db = SessionLocal()
    try:
        gen_ref = db.query(GenerationReference).filter(
            GenerationReference.id == generation_id
        ).first()

        if not gen_ref:
            return None

        content = None
        if MONGO_AVAILABLE and os.getenv("MONGO_URI") and gen_ref.mongo_document_id:
            from bson.objectid import ObjectId
            client = MongoClient(os.getenv("MONGO_URI"))
            db_mongo = client["tri9t"]
            collection = db_mongo["artifacts"]
            doc = collection.find_one({"_id": ObjectId(gen_ref.mongo_document_id)})
            if doc:
                content = doc["generated_content"]
        elif gen_ref.json_file_path and os.path.exists(gen_ref.json_file_path):
            with open(gen_ref.json_file_path, "r") as f:
                data = json.load(f)
                content = data["generated_content"]

        if content:
            return {
                "id": gen_ref.id,
                "selection_id": gen_ref.selection_id,
                "artifact_type": gen_ref.artifact_type,
                "generated_content": content,
                "source_hash": gen_ref.source_hash,
                "created_at": gen_ref.created_at
            }
        else:
            return None
    finally:
        db.close()


def check_staleness(generation_id: int):
    db = SessionLocal()
    try:
        gen_ref = db.query(GenerationReference).filter(
            GenerationReference.id == generation_id
        ).first()

        if not gen_ref:
            return None

        selection = db.query(Selection).filter(Selection.id == gen_ref.selection_id).first()
        nodes = get_selection_nodes(selection.id)
        current_hash = compute_source_hash(nodes)

        changed_nodes = []
        if current_hash != gen_ref.source_hash:
            from app.services.selection_service import get_selection_node_ids
            node_ids = get_selection_node_ids(selection.id)
            db_nodes = db.query(GenerationReference).filter().all()  # dummy
            for node in nodes:
                if node.content_hash:
                    pass
            # Compare each node's current hash with what? We don't store individual node hashes in gen ref,
            # so let's just mark stale if overall hash is different
            changed_nodes = [n.id for n in nodes]

        return {
            "stale": current_hash != gen_ref.source_hash,
            "changed_nodes": changed_nodes if current_hash != gen_ref.source_hash else []
        }
    finally:
        db.close()
