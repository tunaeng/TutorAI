from fastapi import APIRouter, Depends
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.education import Assignment
from datetime import datetime, timedelta, timezone

import json
from pathlib import Path

MOSCOW_TZ = timezone(timedelta(hours=3))

def get_days_ago_start(days_ago: int):
    now_msk = datetime.now(MOSCOW_TZ)
    target_date = now_msk - timedelta(days=days_ago)
    target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return target_date

# Получение фактов недели на студента
router = APIRouter(prefix="/students", tags=["students"])

@router.get("/facts")
async def get_weekly_facts(student_id: str = None, period: int = 7, db: AsyncSession = Depends(get_db)):
    # period_start = get_days_ago_start(period)
    # query = select(Assignment).where(Assignment.submitted_at >= period_start)

    # if student_id:
    #     query = query.where(Assignment.student_id == student_id)
    
    # result = await db.execute(query)
    # facts = result.scalars.all()

    # return [{
    #         "id": a.student_id,
    #         "grade": a.grade, 
    #         "submitted_at": a.submitted_at
    #         } 
    #         for a in facts]

    mock_path = Path("app/api/v1/mock.json")
    mock_data = json.loads(mock_path.read_text())

    student = next((s for s in mock_data["students"] if s["student_id"] == student_id), None)
    if not student:
        return {"error": f"Student with id {student_id} not found"}

    return [
        {
            "id": student["student_id"],
            "grade": a["grade"],
            "submitted_at": a["submitted_at"]
        }
        for a in student["assignments"]
    ]