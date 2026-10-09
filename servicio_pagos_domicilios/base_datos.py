from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL_BASE_DATOS = "postgresql+psycopg2://postgres:postgres@postgres_db:5432/bd_restaurante"

engine = create_engine(URL_BASE_DATOS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()