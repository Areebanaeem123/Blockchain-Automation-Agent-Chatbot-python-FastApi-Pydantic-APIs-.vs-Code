import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("SENDER_EMAIL")        # your Gmail address
EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASS")  # your Gmail app password

def send_alert_email(to_email, coin, threshold):
    subject = "🚨 Price Alert Set!"
    body = f"""
    Hello ! Hope you are doing great !
    ✅ Your alert has been set!
    We’ll notify you when {coin.title()} crosses ${threshold:,}.
    Thank you for using Blockchain Auto Agent 🚀
    """
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        return True, f"📧 Confirmation email sent to {to_email}"
    except Exception as e:
        return False, f"❌ Email failed: {e}"
