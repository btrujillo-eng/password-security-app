from backend.app.api.v1.routers import password_security, repository, health
from backend.app.api.v1.routers import password_security, repository, health, auth

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI(
    title="Password Security APP",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(password_security.router)
app.include_router(repository.router)
app.include_router(health.router)
app.include_router(auth.router)