from fastapi import APIRouter, HTTPException
from app.services.version_compare import compare_versions

router = APIRouter(
    prefix="/compare",
    tags=["Version Comparison"]
)


@router.get("/{version1}/{version2}")
def compare(version1: int, version2: int):
    result = compare_versions(version1, version2)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="One or both versions not found"
        )

    return result