from database import SessionLocal
from models import ServiceProvider, Request

def register_provider(name, contact, skill):
    db = SessionLocal()
    try:
        provider = ServiceProvider(name=name, contact=contact, skill=skill)
        db.add(provider)
        db.commit()
    finally:
        db.close()

def request_service(user_id, service_type):
    db = SessionLocal()
    try:
        new_request = Request(user_id=user_id, service_type=service_type, status="Pending")
        db.add(new_request)
        db.commit()
    finally:
        db.close()
