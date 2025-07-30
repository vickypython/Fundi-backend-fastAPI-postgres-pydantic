from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
DATABASE_URL='sqlite:///./fundi_app.db'
engine=create_engine(DATABASE_URL)
engine_new=create_async_engine(DATABASE_URL,pool_size=30)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bing=engine,)
Base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def get_dbs():
    with SessionLocal as session:
        yield session
        