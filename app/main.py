from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.admin.views import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings

app = FastAPI(
    title="AI Tutor API",
    version="1.0.0",
    description="Backend для AI Tutor системы"
)

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