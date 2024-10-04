import smtplib
import random
import string

def generate_otp() -> str:
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email: str):
    otp = generate_otp()
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    
    # Set up the SMTP server
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        message = f"Your OTP is: {otp}"
        server.sendmail(sender_email, email, message)

    return otp
