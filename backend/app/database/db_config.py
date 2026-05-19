from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

_ = load_dotenv()

db_url = os.getenv("DATABASE_SQLITE_URL")
if not db_url:
    raise RuntimeError("The database URL could not be found")

connect_agrs = {"check_same_thread": False} if 'sqlite' in db_url else {}

engine = create_engine(
    db_url, connect_args= connect_agrs
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)