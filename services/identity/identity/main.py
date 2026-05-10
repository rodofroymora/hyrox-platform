from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


app = FastAPI(
    title="Identity Service",
    description="HYROX Performance Platform — Identity Service",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Verifica que el servicio está operativo."""
    return HealthResponse(status="ok")
