from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SelectionCreate(BaseModel):
    selection_name: str
    version_id: int
    node_ids: List[int]


class SelectionNodeResponse(BaseModel):
    id: int
    node_id: int


class SelectionResponse(BaseModel):
    id: int
    selection_name: str
    version_id: int
    created_at: datetime
    node_ids: List[int]


class GenerateRequest(BaseModel):
    selection_id: int
    artifact_type: str


class GeneratedArtifactResponse(BaseModel):
    id: int
    selection_id: int
    artifact_type: str
    generated_content: str
    source_hash: str
    created_at: datetime


class StalenessResponse(BaseModel):
    stale: bool
    changed_nodes: List[int]
