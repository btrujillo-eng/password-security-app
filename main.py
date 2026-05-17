from backend.app.api.v1.routers import repository, password_security, health

from fastapi import FastAPI

app = FastAPI(
    title="Password Security APP",
    version="1.0.0"
)

app.include_router(password_security.router)

app.include_router(repository.router)

app.include_router(health.router)