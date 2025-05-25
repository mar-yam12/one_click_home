import streamlit as st
import os
from dotenv import load_dotenv
from auth import verify_login
from database import get_user, add_user, get_all_skilled_persons, init_db
from payment import create_payment_session
from dashboard import show_user_dashboard, show_skilled_dashboard
from request_handler import book_service
from ratings import rate_service
from PIL import Image

load_dotenv()
init_db()
st.set_page_config(page_title="One-Click Home Services", layout="wide", page_icon="🏠")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = None
    st.session_state.user_type = None

def login_section():
    st.sidebar.title("🔐 Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user = verify_login(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.email = user.email
            st.session_state.user_type = user.type
            st.success("Login successful!")
            st.rerun()  # Refresh UI after login
        else:
            st.error("Invalid credentials!")

    st.sidebar.markdown("---")
    st.sidebar.title("📝 Register")

    new_name = st.sidebar.text_input("Name")
    new_email = st.sidebar.text_input("Email", key="reg_email")
    new_password = st.sidebar.text_input("Password", type="password", key="reg_pass")
    user_type = st.sidebar.selectbox("Register As", ["User", "Skilled Person"])
    contact = st.sidebar.text_input("Contact No")
    city = st.sidebar.text_input("City")

    image = st.sidebar.file_uploader("Profile Image", type=["jpg", "png"])

    if st.sidebar.button("Register"):
        if new_name and new_email and new_password:
            from auth import create_user  # avoid circular import
            try:
                user = create_user(new_name, new_email, new_password, user_type, contact, city)
                if image:
                    os.makedirs("profile_images", exist_ok=True)
                    with open(f"profile_images/{new_email}.jpg", "wb") as f:
                        f.write(image.read())
                st.success("Registered successfully! Please login.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill all required fields.")

def logout():
    st.session_state.logged_in = False
    st.session_state.email = None
    st.session_state.user_type = None
    st.rerun()  # Refresh UI after logout

def main_app():
    st.title("🏠 One-Click Home Services")

    if st.session_state.user_type == "User":
        show_user_dashboard(st.session_state.email)
    else:
        show_skilled_dashboard(st.session_state.email)

    st.markdown("---")
    st.subheader("🧑‍🔧 Available Skilled Persons")

    city_filter = st.selectbox("Select City", ["All", "Karachi", "Lahore", "Islamabad", "Peshawar"])

    skilled_persons = get_all_skilled_persons()

    filtered = [
        p for p in skilled_persons
        if city_filter == "All" or (p.city and p.city.lower() == city_filter.lower())
    ]

    for skilled in filtered:
        st.markdown(f"### 👷 {skilled.name} ({skilled.type})")
        st.markdown(f"📍 City: {skilled.city}")
        st.markdown(f"📞 Contact: {skilled.contact}")
        st.markdown(f"📧 Email: {skilled.email}")

        img_path = f"profile_images/{skilled.email}.jpg"
        if os.path.exists(img_path):
            st.image(Image.open(img_path), width=100)

        if st.session_state.user_type == "User":
            with st.expander("📋 Book This Service"):
                if st.button(f"Book {skilled.name}", key=f"book_{skilled.email}"):
                    booked = book_service(
                        user_email=st.session_state.email,
                        skilled_email=skilled.email,
                        service=skilled.type
                    )
                    if booked:
                        st.success("Request sent successfully!")
                    else:
                        st.error("Booking failed!")

                st.markdown("💳 **Make Payment (Optional)**")
                if st.button(f"Pay $50 for {skilled.email}", key=f"pay_{skilled.email}"):
                    url = create_payment_session(
                        amount=50,
                        success_url="http://localhost:8501",
                        cancel_url="http://localhost:8501"
                    )
                    st.markdown(f"[👉 Click to Pay]({url})")

                st.markdown("⭐ **Rate This Skilled Person**")
                rating = st.slider(f"Rating for {skilled.name}", 1, 5, 5, key=f"rate_slider_{skilled.email}")
                feedback = st.text_area(f"Feedback for {skilled.name}", key=f"feedback_{skilled.email}")
                if st.button(f"Submit Rating for {skilled.email}", key=f"submit_rate_{skilled.email}"):
                    rate_service(st.session_state.email, skilled.email, rating, feedback)
                    st.success("Thanks for your feedback!")

# Run the app logic
if not st.session_state.logged_in:
    login_section()
else:
    st.sidebar.button("Logout", on_click=logout)
    main_app()
