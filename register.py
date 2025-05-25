import os
from streamlit import st

image = st.file_uploader("Upload Profile Picture", type=["png", "jpg"])

if image:
    email = st.text_input("Enter your email for image naming")  
    if email:
        os.makedirs("profile_images", exist_ok=True)
        with open(f"profile_images/{email}.jpg", "wb") as f:
            f.write(image.read())
        st.success("Image uploaded successfully!")
