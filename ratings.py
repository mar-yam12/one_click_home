from database import SessionLocal


def save_rating(rating_data: dict):
    db = SessionLocal()
    db.close()

def rate_service(user_email, skilled_email, rating, feedback):

    save_rating({
        "user": user_email,
        "skilled": skilled_email,
        "rating": rating,
        "feedback": feedback
    })
