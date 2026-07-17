from app.database.database import SessionLocal
from app.models.models import Selection, SelectionNode, Node, DocumentVersion
from app.schemas.schemas import SelectionCreate
from typing import List


def create_selection(selection_data: SelectionCreate):
    db = SessionLocal()
    try:
        version = db.query(DocumentVersion).filter(
            DocumentVersion.id == selection_data.version_id
        ).first()
        if not version:
            return None, "Version not found"

        valid_node_ids = []
        for node_id in selection_data.node_ids:
            node = db.query(Node).filter(
                Node.id == node_id,
                Node.version_id == selection_data.version_id
            ).first()
            if not node:
                return None, f"Node {node_id} not found or not in specified version"
            valid_node_ids.append(node_id)

        selection = Selection(
            selection_name=selection_data.selection_name,
            version_id=selection_data.version_id
        )
        db.add(selection)
        db.flush()

        for node_id in valid_node_ids:
            selection_node = SelectionNode(
                selection_id=selection.id,
                node_id=node_id
            )
            db.add(selection_node)

        db.commit()
        db.refresh(selection)

        return selection, None
    finally:
        db.close()


def get_selections():
    db = SessionLocal()
    try:
        return db.query(Selection).all()
    finally:
        db.close()


def get_selection(selection_id: int):
    db = SessionLocal()
    try:
        return db.query(Selection).filter(
            Selection.id == selection_id
        ).first()
    finally:
        db.close()


def get_selection_node_ids(selection_id: int):
    db = SessionLocal()
    try:
        selection_nodes = db.query(SelectionNode).filter(
            SelectionNode.selection_id == selection_id
        ).all()
        return [sn.node_id for sn in selection_nodes]
    finally:
        db.close()


def get_selection_nodes(selection_id: int):
    db = SessionLocal()
    try:
        selection = db.query(Selection).filter(Selection.id == selection_id).first()
        if not selection:
            return None

        node_ids = get_selection_node_ids(selection_id)
        nodes = db.query(Node).filter(Node.id.in_(node_ids)).all()
        return nodes
    finally:
        db.close()
