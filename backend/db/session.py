from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL

# pool_size/max_overflow raised above SQLAlchemy's defaults (5 + 10 = 15) — the job-folder watcher
# (services/job_folder_watcher.py) can now have up to MAX_WORKERS=10 threads each holding a
# session open for the duration of one CV's pipeline (~166s), on top of normal request traffic.
engine = create_engine(DATABASE_URL, pool_size=15, max_overflow=15)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all() -> None:
    Base.metadata.create_all(bind=engine)
