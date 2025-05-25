import os
from streamlit import st

image = st.file_uploader("Upload Profile Picture", type=["png", "jpg"])

if image:
    # For file naming, use a better identifier (like email), pass it properly
    # Example: email variable must be passed to this file or function
    # Here just showing how to save
    email = st.text_input("Enter your email for image naming")  # You need to implement how to pass email
    if email:
        os.makedirs("profile_images", exist_ok=True)
        with open(f"profile_images/{email}.jpg", "wb") as f:
            f.write(image.read())
        st.success("Image uploaded successfully!")
