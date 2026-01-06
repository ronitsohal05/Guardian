import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
SENDER_NAME = os.getenv("SENDER_NAME", "Guardian")

def send_notification_email(
    recipient_email: str,
    store_name: str,
    item: str,
    distance_km: float,
    store_location: Optional[dict] = None
) -> bool:
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("[email_service] SMTP credentials not configured, skipping email")
        return False
    
    try:
        subject = f"🎉 {store_name} has surplus {item}!"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2ecc71;">Good news! Surplus food available near you</h2>
                
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Store:</strong> {store_name}</p>
                    <p><strong>Item:</strong> <span style="font-size: 1.2em; color: #e74c3c;">{item.title()}</span></p>
                    <p><strong>Distance:</strong> {distance_km:.1f} km away</p>
                    {f'<p><strong>Location:</strong> {store_location}</p>' if store_location else ''}
                </div>
                
                <p>This item matches your preferences! Visit the store to claim your surplus food.</p>
                
                <p style="color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
                    Guardian • Surplus Food Notification
                </p>
            </body>
        </html>
        """
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = recipient_email
        
        text_body = f"""
        Good news! Surplus food available near you
        
        Store: {store_name}
        Item: {item}
        Distance: {distance_km:.1f} km away
        {f'Location: {store_location}' if store_location else ''}
        
        This item matches your preferences! Visit the store to claim your surplus food.
        """
        
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"[email_service] Email sent to {recipient_email} about {item} from {store_name}")
        return True
    
    except Exception as e:
        print(f"[email_service] Failed to send email to {recipient_email}: {str(e)}")
        return False


def send_verification_email(recipient_email: str, token: str) -> bool:
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("[email_service] SMTP credentials not configured, skipping verification email")
        return False
    
    try:
        subject = "Verify your Guardian account"
        verification_link = f"https://guardian.local/verify?token={token}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2>Welcome to Guardian!</h2>
                <p>Please verify your email address to start receiving surplus food notifications.</p>
                
                <p style="margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="background-color: #2ecc71; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Verify Email
                    </a>
                </p>
                
                <p style="color: #7f8c8d; font-size: 0.9em;">
                    Guardian • Surplus Food Network
                </p>
            </body>
        </html>
        """
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = recipient_email
        
        text_body = f"Please verify your email: {verification_link}"
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"[email_service] Verification email sent to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"[email_service] Failed to send verification email to {recipient_email}: {str(e)}")
        return False
