import smtplib
import os
import sys
from email.mime.text import MIMEText
from dotenv import load_dotenv

# הוספת נתיב לפרויקט (לפי הצורך)
sys.path.append(r'C:\meshi\ApartmentHunterBot')

# טען את כל הערכים מה-.env
load_dotenv()

# קריאה של משתנים מה-.env
APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")          # סיסמה לאפליקציה
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")               # כתובת השולח
RECIPIENTS = os.getenv("EMAIL_RECIPIENTS")  # רשימת מקבלים מופרדת בפסיקים

# תוכן המייל
BODY = "Hello my name is Slim Shady"
SUBJECT = "פוסטים לדירות בפייסבוק"

def format_posts_for_email(posts):
    """
    Formats a list of posts (documents) into a single string for email body.

    Parameters:
    - posts: A list of documents where each document contains 'link' and 'content'.

    Returns:
    - A formatted string that can be used as the body of an email (HTML).
    """
    formatted_message = "<div style='direction: rtl; text-align: right;'>\n"
    for post in posts:
        formatted_message += f"קישור - {post['link']}<br>\n"
        formatted_message += f"{post['content']}<br>\n"
        formatted_message += "----------------<br>\n"
    formatted_message += "</div>\n"
    return formatted_message

def send_email(subject, body):
    """
    Send an HTML email using Gmail SMTP server.
    """
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(RECIPIENTS)
    
    # חיבור ל-SMTP של Gmail דרך SSL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(SENDER_EMAIL, APP_PASSWORD)
        smtp_server.sendmail(from_addr=SENDER_EMAIL, to_addrs=RECIPIENTS, msg=msg.as_string())
        print("Message sent successfully")

 
