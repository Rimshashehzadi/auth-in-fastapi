
# from fastapi import FastAPI, HTTPException, Form
# from pydantic import EmailStr

# app = FastAPI()

# # Simulated database of users (in-memory list for demonstration)
# # users_db = []
# users_db: list[dict[str, str]] = []

# # API endpoint for handling signup form submission
# @app.post("/signup/")
# async def signup(
#     email: EmailStr = Form(...),  # Expect email as form data
#     password: str = Form(...),  # Expect password as form data
#     confirm_password: str = Form(...)  # Expect confirm password as form data
# ):
#     # Check if password length is valid
#     if len(password) < 8 or len(confirm_password) < 8:
#         raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

#     # Check if passwords match
#     if password != confirm_password:
#         raise HTTPException(status_code=400, detail="Passwords do not match")

#     # Check if the email is already registered
#     for user in users_db:
#         if user["email"] == email:
#             raise HTTPException(status_code=400, detail="Email already registered")

#     # Simulate adding the user to the database
#     users_db.append({"email": email, "password": password})

#     return {"message": "User signed up successfully", "email": email}

# # API endpoint to get all emails (for testing purposes)
# @app.get("/emails/")
# def get_all_emails():
#     emails = [user["email"] for user in users_db]
#     return {"emails": emails}

import random
import smtplib
from fastapi import FastAPI, HTTPException, Form
from pydantic import EmailStr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# Simulated database of users (in-memory list for demonstration)
users_db: list[dict[str, str]] = []

# Function to generate a random OTP
def generate_otp():
    return str(random.randint(100000, 999999))  # Generate a 6-digit OTP

# Function to send OTP via email
def send_otp_via_email(email: str, otp: str):
    sender_email = "your-email@example.com"  # Your email address
    sender_password = "your-email-password"  # Your email account password

    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}. It will expire in 5 minutes."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Setup the SMTP server
        server = smtplib.SMTP('smtp.example.com', 587)  # Replace with your SMTP server details
        server.starttls()  # Enable encryption
        server.login(sender_email, sender_password)
        
        # Send email
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP via email")

# API endpoint for handling signup form submission
@app.post("/signup/")
async def signup(
    email: EmailStr = Form(...),  # Expect email as form data
    password: str = Form(...),  # Expect password as form data
    confirm_password: str = Form(...)  # Expect confirm password as form data
):
    # Check if password length is valid
    if len(password) < 8 or len(confirm_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    # Check if passwords match
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if the email is already registered
    for user in users_db:
        if user["email"] == email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Generate OTP
    otp = generate_otp()

    # Send OTP to the user's email
    send_otp_via_email(email, otp)

    # Simulate adding the user to the database with the OTP
    users_db.append({"email": email, "password": password, "otp": otp})

    return {"message": "User signed up successfully, OTP sent to your email", "email": email}

# API endpoint to get all emails (for testing purposes)
@app.get("/emails/")
def get_all_emails():
    emails = [user["email"] for user in users_db]
    return {"emails": emails}
