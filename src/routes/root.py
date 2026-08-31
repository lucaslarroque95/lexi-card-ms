from fastapi import APIRouter

router = APIRouter(tags=["Root"])

@router.get("/")
def root():
    return {
        "name": "Vocabulary ms",
        "version": "1.0.0",
        "message": "API is running"
    }


