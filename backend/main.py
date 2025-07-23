from api.endpoints import router as api_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination

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
app.include_router(api_router, prefix="/api")

add_pagination(app)
