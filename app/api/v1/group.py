from fastapi import APIRouter

# Запрос конфигурации группы/периода/программы
router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/config")
async def get_group_config(stream_id: str = None, week: int = None, module_id: str = None):
    return {"message": "Group API - coming soon"}