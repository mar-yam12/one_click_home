import stripe
from dotenv import load_dotenv
import os

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
print("Stripe Key:", os.getenv("STRIPE_SECRET_KEY"))

def create_payment_session(amount, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': amount * 100,
                'product_data': {'name': 'Home Essential Service'}
            },
            'quantity': 1
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url
    )
    return session.url
