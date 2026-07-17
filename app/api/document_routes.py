from fastapi import APIRouter, HTTPException

from app.services.document_service import (
    get_documents,
    get_document,
    get_versions,
    get_nodes,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("/")
def list_documents():
    documents = get_documents()

    return [
        {
            "id": d.id,
            "name": d.name,
            "description": d.description,
        }
        for d in documents
    ]


@router.get("/{document_id}")
def get_document_details(document_id: int):
    document = get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": document.id,
        "name": document.name,
        "description": document.description,
    }


@router.get("/{document_id}/versions")
def list_versions(document_id: int):
    versions = get_versions(document_id)

    return [
        {
            "id": v.id,
            "version_number": v.version_number,
            "file_name": v.file_name,
        }
        for v in versions
    ]


@router.get("/versions/{version_id}/nodes")
def list_nodes(version_id: int):
    nodes = get_nodes(version_id)

    return [
        {
            "id": n.id,
            "section": n.section_number,
            "heading": n.heading,
            "level": n.level,
            "body": n.body,
        }
        for n in nodes
    ]