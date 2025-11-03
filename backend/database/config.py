import os

from dotenv import load_dotenv
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from setting.config import get_settings

settings = get_settings()

# Create engine with statement cache disabled for pgbouncer compatibility
engine = create_async_engine(
    settings.database_url, 
    echo=True,
    connect_args={"prepared_statement_cache_size": 0}
)

# Create session
async_session = sessionmaker(
    engine, expire_on_commit=False, autocommit=False, class_=AsyncSession
)

Base = declarative_base()

database = Database(settings.database_url)
