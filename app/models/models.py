from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    versions = relationship("DocumentVersion", back_populates="document")


class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    version_number = Column(Integer, nullable=False)
    file_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="versions")
    nodes = relationship("Node", back_populates="version")


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)

    version_id = Column(Integer, ForeignKey("document_versions.id"))
    parent_id = Column(Integer, ForeignKey("nodes.id"), nullable=True)

    logical_node_id = Column(String)
    heading = Column(String, nullable=False)
    body = Column(Text)

    level = Column(Integer)
    section_number = Column(String)

    content_hash = Column(String)

    node_order = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    version = relationship("DocumentVersion", back_populates="nodes")

    parent = relationship(
        "Node",
        remote_side=[id],
        backref="children"
    )


class Selection(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True, index=True)
    selection_name = Column(String, nullable=False)
    version_id = Column(Integer, ForeignKey("document_versions.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    selection_nodes = relationship("SelectionNode", back_populates="selection")
    generation_references = relationship("GenerationReference", back_populates="selection")


class SelectionNode(Base):
    __tablename__ = "selection_nodes"

    id = Column(Integer, primary_key=True, index=True)

    selection_id = Column(Integer, ForeignKey("selections.id"))

    node_id = Column(Integer, ForeignKey("nodes.id"))

    selection = relationship("Selection", back_populates="selection_nodes")


class GenerationReference(Base):
    __tablename__ = "generation_references"

    id = Column(Integer, primary_key=True, index=True)

    selection_id = Column(Integer, ForeignKey("selections.id"))

    artifact_type = Column(String, nullable=False)

    mongo_document_id = Column(String, nullable=True)
    json_file_path = Column(String, nullable=True)

    source_hash = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    selection = relationship("Selection", back_populates="generation_references")