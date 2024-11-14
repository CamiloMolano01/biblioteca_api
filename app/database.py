from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .models import models
from . import config

envs = config.Settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{envs.db_user}:{envs.db_password}@{envs.db_host}:{envs.db_port}/{envs.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    models.Base.metadata.create_all(bind=engine)
    if not envs.env == "prod":
        from .sample_data import load_sample_data

        session = SessionLocal()
        try:
            print("Loading sample data...")
            load_sample_data(session)
        finally:
            session.close()
