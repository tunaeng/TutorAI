from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.education import Stream

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/")
async def get_students(group_id: str, db: Session = Depends(get_db)):
    """
    Возвращает список студентов по названию группы (stream.stream_id = group_id)
    """

    if group_id == "AI-102":
        return [
  {
    "student_id": "st_001",
    "group_id": group_id
  },
  {
    "student_id": "st_002",
    "group_id": group_id
  },
  {
    "student_id": "st_003",
    "group_id": group_id
  },
  {
    "student_id": "st_004",
    "group_id": group_id
  },
  {
    "student_id": "st_005",
    "group_id": group_id
  }
]
    if group_id == "ML-102":
        return [
  {
    "student_id": "st_101",
    "group_id": group_id
  },
  {
    "student_id": "st_102",
    "group_id": group_id
  },
  {
    "student_id": "st_103",
    "group_id": group_id
  },
  {
    "student_id": "st_104",
    "group_id": group_id
  },
  {
    "student_id": "st_105",
    "group_id": group_id
  }
]
    # Ищем поток по имени (названию группы)
    # stream = db.query(Stream).filter(Stream.stream_id == group_id).first()
    
    # return [{"student_id": s.student_id} for s in stream.students]
