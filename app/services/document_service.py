from app.database.database import SessionLocal
from app.models.models import Document, DocumentVersion, Node


def get_documents():
    db = SessionLocal()
    try:
        return db.query(Document).all()
    finally:
        db.close()


def get_document(document_id: int):
    db = SessionLocal()
    try:
        return db.query(Document).filter(
            Document.id == document_id
        ).first()
    finally:
        db.close()


def get_versions(document_id: int):
    db = SessionLocal()
    try:
        return db.query(DocumentVersion).filter(
            DocumentVersion.document_id == document_id
        ).all()
    finally:
        db.close()


def get_nodes(version_id: int):
    db = SessionLocal()
    try:
        return (
            db.query(Node)
            .filter(Node.version_id == version_id)
            .order_by(Node.node_order)
            .all()
        )
    finally:
        db.close()
from sqlalchemy import or_


def search_nodes(query: str):
    db = SessionLocal()

    try:
        return (
            db.query(Node)
            .filter(
                or_(
                    Node.heading.ilike(f"%{query}%"),
                    Node.body.ilike(f"%{query}%"),
                    Node.section_number.ilike(f"%{query}%"),
                )
            )
            .order_by(Node.node_order)
            .all()
        )

    finally:
        db.close()