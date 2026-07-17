from fastapi import APIRouter, HTTPException
from app.schemas.schemas import GenerateRequest, GeneratedArtifactResponse, StalenessResponse
from app.services.selection_service import get_selection, get_selection_nodes
from app.llm.generator import (
    build_prompt,
    call_llm,
    compute_source_hash,
    store_artifact,
    retrieve_artifact,
    check_staleness
)

router = APIRouter(
    tags=["Generation"]
)


@router.post("/generate", response_model=GeneratedArtifactResponse)
def generate_artifact(request: GenerateRequest):
    selection = get_selection(request.selection_id)
    if not selection:
        raise HTTPException(status_code=404, detail="Selection not found")

    nodes = get_selection_nodes(request.selection_id)
    if not nodes:
        raise HTTPException(status_code=400, detail="No nodes in selection")

    prompt = build_prompt(nodes, request.artifact_type)
    generated_content = call_llm(prompt)
    source_hash = compute_source_hash(nodes)

    gen_ref = store_artifact(
        selection_id=request.selection_id,
        artifact_type=request.artifact_type,
        content=generated_content,
        source_hash=source_hash
    )

    return GeneratedArtifactResponse(
        id=gen_ref.id,
        selection_id=gen_ref.selection_id,
        artifact_type=gen_ref.artifact_type,
        generated_content=generated_content,
        source_hash=gen_ref.source_hash,
        created_at=gen_ref.created_at
    )


@router.get("/generated/{generation_id}", response_model=GeneratedArtifactResponse)
def get_generated_artifact(generation_id: int):
    artifact = retrieve_artifact(generation_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Generated artifact not found")
    return GeneratedArtifactResponse(**artifact)


@router.get("/staleness/{generation_id}", response_model=StalenessResponse)
def check_artifact_staleness(generation_id: int):
    staleness = check_staleness(generation_id)
    if staleness is None:
        raise HTTPException(status_code=404, detail="Generation reference not found")
    return StalenessResponse(**staleness)
