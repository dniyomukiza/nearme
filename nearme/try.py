import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def otp_generate():
    return random.randint(10000, 99999)
def send_email(email):
    try:
        otp = otp_generate()
        # Retrieve environment variables
        conf_email = os.environ.get("CONF_EMAIL")
        conf_code = os.environ.get("CONF_CODE")
        sender_email = os.environ.get("SENDER_EMAIL")
        if not conf_email or not conf_code or not sender_email:
            return "Environment variables not properly set."
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, conf_code)

        # Create the email content
        subject = 'OTP code'
        body = f'Verification code: {otp_generate()}'
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        return "OTP sent!"
    except Exception as e:
        return f"Failed to send OTP: {e}"

resp = send_email("didyom1@gmail.com")
print("message ",resp)
