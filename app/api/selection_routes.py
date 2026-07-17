from fastapi import APIRouter, HTTPException
from app.schemas.schemas import SelectionCreate, SelectionResponse
from app.services.selection_service import (
    create_selection,
    get_selections,
    get_selection,
    get_selection_node_ids
)

router = APIRouter(
    prefix="/selections",
    tags=["Selections"]
)


@router.post("/", response_model=SelectionResponse)
def create_new_selection(selection: SelectionCreate):
    new_selection, error = create_selection(selection)
    if error:
        raise HTTPException(status_code=400, detail=error)
    node_ids = get_selection_node_ids(new_selection.id)
    return SelectionResponse(
        id=new_selection.id,
        selection_name=new_selection.selection_name,
        version_id=new_selection.version_id,
        created_at=new_selection.created_at,
        node_ids=node_ids
    )


@router.get("/", response_model=list[SelectionResponse])
def list_selections():
    selections = get_selections()
    return [
        SelectionResponse(
            id=s.id,
            selection_name=s.selection_name,
            version_id=s.version_id,
            created_at=s.created_at,
            node_ids=get_selection_node_ids(s.id)
        )
        for s in selections
    ]


@router.get("/{selection_id}", response_model=SelectionResponse)
def get_selection_details(selection_id: int):
    selection = get_selection(selection_id)
    if not selection:
        raise HTTPException(status_code=404, detail="Selection not found")
    node_ids = get_selection_node_ids(selection_id)
    return SelectionResponse(
        id=selection.id,
        selection_name=selection.selection_name,
        version_id=selection.version_id,
        created_at=selection.created_at,
        node_ids=node_ids
    )
