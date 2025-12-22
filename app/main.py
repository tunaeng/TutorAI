from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.admin.views import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
import traceback
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Tutor API",
    version="1.0.0",
    description="Backend для AI Tutor системы"
)

# Middleware для логирования ошибок
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Exception in {request.url.path}: {e}")
        logger.error(traceback.format_exc())
        raise

# Сессии для аутентификации админ-панели
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Админка
admin = setup_admin(app)

@app.get("/")
def root():
    """Редирект на админку"""
    return RedirectResponse(url="/admin")

@app.get("/health")
def health_check():
    return {"status": "ok"}