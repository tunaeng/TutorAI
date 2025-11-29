from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.education import Stream
import json
from pathlib import Path

router = APIRouter(prefix="/config", tags=["config"])

@router.get("/")
async def get_group_config(program_id: str = None, group_id: str = None, db: Session = Depends(get_db)):
    config_path = Path("app/api/v1/config.json")
    config = json.loads(config_path.read_text())

    # Загружаем базовую структуру
    if not program_id:
        return config

    program = config["programs"].get(program_id)
    if not program:
        return {"error": "Program not found"}

    if not group_id:
        return program

    group = program.get("groups", {}).get(group_id)
    if not group:
        return {"error": "Group not found"}

    # Получаем дату начала из базы
    stream = db.query(Stream).filter(Stream.name == group_id).first()
    start_date = stream.start_date if stream else None

    final = program.copy()
    if group:
        final.update(group)
    final["start_date"] = str(start_date) if start_date else None
    return final
