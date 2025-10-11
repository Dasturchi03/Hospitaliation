from app.models import *
from app.core.db import engine
from app.db.base import Base


async def create_db():
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully!")
