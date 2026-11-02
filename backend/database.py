from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from settings import settings

DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL, echo=settings.is_local, hide_parameters=True
)

SessionLocal = sessionmaker(autocommit=False, bind=engine, class_=Session)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
