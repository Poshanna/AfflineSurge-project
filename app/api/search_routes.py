from fastapi import APIRouter, Query
from app.services.document_service import search_nodes

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/")
def search(q: str = Query(..., description="Search keyword")):

    results = search_nodes(q)

    return [
        {
            "section": node.section_number,
            "heading": node.heading,
            "level": node.level,
            "body": node.body,
        }
        for node in results
    ]