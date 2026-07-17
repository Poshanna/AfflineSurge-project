from app.database.database import SessionLocal
from app.models.models import Document, DocumentVersion, Node
from app.services.hash_service import generate_content_hash


def ingest_document(document_name, version_number, file_name, sections):

    db = SessionLocal()

    try:

        document = db.query(Document).filter(
            Document.name == document_name
        ).first()

        if not document:
            document = Document(
                name=document_name
            )
            db.add(document)
            db.commit()
            db.refresh(document)

        version = DocumentVersion(
            document_id=document.id,
            version_number=version_number,
            file_name=file_name
        )

        db.add(version)
        db.commit()
        db.refresh(version)

        for index, section in enumerate(sections):

            node = Node(
                version_id=version.id,
                parent_id=None,
                logical_node_id=section["section_number"],
                heading=section["title"],
                body=section["content"],
                level=section["level"],
                section_number=section["section_number"],
                content_hash=generate_content_hash(section["content"]),
                node_order=index + 1
            )

            db.add(node)

        db.commit()

        print(f"Inserted {len(sections)} sections successfully.")

    finally:
        db.close()