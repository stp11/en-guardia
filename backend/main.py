from api.endpoints import router as api_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination

app = FastAPI()
add_pagination(app)
app.include_router(api_router, prefix="/api")
