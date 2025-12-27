import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqladmin import Admin

from admin import AdminAuth
from api.endpoints import router as api_router
from database import engine
from models import CategoryAdmin, EpisodeAdmin

ADMIN_PATH = os.environ.get("ADMIN_PATH", "/admin")
ADMIN_SECRET_KEY = os.environ.get("ADMIN_SECRET_KEY")
ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app = FastAPI(
    docs_url="/api/docs",
    redoc_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

authentication_backend = AdminAuth(secret_key=ADMIN_SECRET_KEY)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
    base_url=ADMIN_PATH,
)

admin.add_view(EpisodeAdmin)
admin.add_view(CategoryAdmin)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
add_pagination(app)


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway and Cloudflare."""
    return {"status": "healthy"}
