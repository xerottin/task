# test.py
from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])

@router.get("")
async def test_endpoint():
    return {"message": "Test endpoint is working!"}