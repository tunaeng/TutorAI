from fastapi import APIRouter

# Получение фактов недели на студента
router = APIRouter(prefix="/students", tags=["students"])

@router.get("/facts")
async def get_weekly_facts(week: int = None, student_id: int = None):
    return {"message": "Facts API - coming soon"}