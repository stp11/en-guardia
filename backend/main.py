import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqladmin import Admin

from admin import AdminAuth
from api.endpoints import router as api_router
from database import engine
from models import CategoryAdmin, EpisodeAdmin

ADMIN_PATH = os.environ.get("ADMIN_PATH", "/admin")
ADMIN_SECRET_KEY = os.environ.get("ADMIN_SECRET_KEY")
ORIGINS = os.environ.get("ALLOWED_ORIGINS")

app = FastAPI(
    docs_url="/api/docs",
    redoc_url=None,
)

authentication_backend = AdminAuth(secret_key=ADMIN_SECRET_KEY)
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
    base_url=ADMIN_PATH,
)

admin.add_view(EpisodeAdmin)
admin.add_view(CategoryAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
add_pagination(app)
