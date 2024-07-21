from fastapi import FastAPI
from app.api.v1.endpoints import funds
from app.db.base import Base
from app.db.session import engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(funds.router, prefix="/api/v1")
