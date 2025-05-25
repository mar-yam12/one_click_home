import bcrypt
from database import SessionLocal
from models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_user(name, email, password, user_type, contact=None, city=None):
    db = SessionLocal()
    try:
        hashed_pw = hash_password(password)
        user = User(
            name=name,
            email=email,
            password=hashed_pw,
            type=user_type,
            contact=contact,
            city=city
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_user_by_email(email):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def verify_login(email, password):
    user = get_user_by_email(email)
    if user and verify_password(password, user.password):
        return user
    return None
