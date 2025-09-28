import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.endpoints import router as api_router

tags_metadata = [
    {
        "name": "episodis",
        "description": "Episodis API",
    }
]

app = FastAPI(
    docs_url="/api/docs",
    redoc_url=None,
    openapi_tags=tags_metadata,
)

origins = os.environ.get("ALLOWED_ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
add_pagination(app)
