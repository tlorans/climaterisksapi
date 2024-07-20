from fastapi import FastAPI
from app.api.v1.endpoints import universe
from app.db import base
from app.db.session import engine

# Create all tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(universe.router, prefix="/api/v1", tags=["universes"])
