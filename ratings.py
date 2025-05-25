from database import SessionLocal

# Assuming you have a Rating model in your models.py, if not you need to add one.
def save_rating(rating_data: dict):
    db = SessionLocal()
    # Implement rating save logic here, add Rating model to models.py if needed
    # For now, just placeholder
    db.close()

def rate_service(user_email, skilled_email, rating, feedback):
    # Save rating logic here, can be implemented once Rating model exists
    save_rating({
        "user": user_email,
        "skilled": skilled_email,
        "rating": rating,
        "feedback": feedback
    })
