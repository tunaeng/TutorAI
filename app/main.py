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
        # Логируем 500 ошибки даже если они не выбросили исключение
        if response.status_code == 500:
            logger.error(f"500 error in {request.url.path} - response status is 500")
        return response
    except Exception as e:
        error_msg = f"Exception in {request.url.path}: {e}\n{traceback.format_exc()}"
        logger.error(error_msg)
        print(f"\n{'='*80}\nERROR:\n{error_msg}\n{'='*80}\n")
        # В режиме DEBUG отдаем текст ошибки в ответ, чтобы проще было отладить
        from fastapi.responses import PlainTextResponse
        if settings.DEBUG:
            return PlainTextResponse(
                f"Error in {request.url.path}:\n{e}\n\n{traceback.format_exc()}",
                status_code=500,
                media_type="text/plain; charset=utf-8",
            )
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