from fastapi import APIRouter

# Выбор слушателей недели 
router = APIRouter(prefix="/students", tags=["students"])

@router.get("/")
async def get_students(week: int = None): # какой параметр передавать?
    return {"message": "Listeners API - coming soon"}