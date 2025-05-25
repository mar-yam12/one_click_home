from database import SessionLocal
from models import Request, User

def add_request(request_data: dict):
    db = SessionLocal()
    try:
        req = Request(
            user_id=request_data.get("user_id"),
            service_type=request_data.get("service"),
            status=request_data.get("status", "Pending")
        )
        db.add(req)
        db.commit()
    finally:
        db.close()

def book_service(user_email, skilled_email, service):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == user_email).first()
        skilled = db.query(User).filter(User.email == skilled_email).first()
        if not user or not skilled:
            return False

        req = Request(
            user_id=user.id,
            service_type=service,
            status="Pending"
        )
        db.add(req)
        db.commit()
        return True
    finally:
        db.close()
