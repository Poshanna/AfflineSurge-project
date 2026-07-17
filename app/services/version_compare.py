from app.database.database import SessionLocal
from app.models.models import DocumentVersion, Node


def compare_versions(version1_number: int, version2_number: int):
    db = SessionLocal()

    try:
        v1 = db.query(DocumentVersion).filter(
            DocumentVersion.version_number == version1_number
        ).first()

        v2 = db.query(DocumentVersion).filter(
            DocumentVersion.version_number == version2_number
        ).first()

        if not v1 or not v2:
            return None

        nodes_v1 = db.query(Node).filter(Node.version_id == v1.id).all()
        nodes_v2 = db.query(Node).filter(Node.version_id == v2.id).all()

        map_v1 = {node.section_number: node for node in nodes_v1}
        map_v2 = {node.section_number: node for node in nodes_v2}

        added = []
        modified = []
        removed = []

        for section, node in map_v2.items():
            if section not in map_v1:
                added.append(section)
            elif map_v1[section].content_hash != node.content_hash:
                modified.append(section)

        for section in map_v1:
            if section not in map_v2:
                removed.append(section)

        return {
            "version1": version1_number,
            "version2": version2_number,
            "added": added,
            "modified": modified,
            "removed": removed
        }

    finally:
        db.close()