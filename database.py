from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_base import Base
from models import User

DATABASE_URL = "sqlite:///home_services.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)


def get_user(email: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def add_user(user_data: dict):
    db = SessionLocal()
    try:
        user = User(
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"],
            type=user_data["type"],
            contact=user_data.get("contact"),
            city=user_data.get("city")
        )
        db.add(user)
        db.commit()
    finally:
        db.close()

def get_all_skilled_persons():
    db = SessionLocal()
    try:
        return db.query(User).filter(User.type == "Skilled Person").all()
    finally:
        db.close()


