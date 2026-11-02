from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import router as api_router
from settings import settings

app = FastAPI(
    docs_url="/api/docs",
    redoc_url=None,
    generate_unique_id_function=lambda route: route.name,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
