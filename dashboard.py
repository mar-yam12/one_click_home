import streamlit as st
from database import SessionLocal
from models import User

def show_user_dashboard(email):
    st.subheader("👥 User Dashboard")
    st.write(f"Welcome, {email}!")
    st.info("You can book services, rate workers, and track your requests.")

def show_skilled_dashboard(email):
    st.subheader("🔧 Skilled Person Dashboard")
    st.write(f"Welcome, {email}!")
    st.info("You can view your bookings and manage your profile.")

def get_user(email: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def get_all_skilled_persons():
    db = SessionLocal()
    try:
        return db.query(User).filter(User.type == "Skilled Person").all()
    finally:
        db.close()
