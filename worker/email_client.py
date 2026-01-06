import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
SENDER_NAME = os.getenv("SENDER_NAME", "Guardian")

def send_match_notification(
    recipient_email: str,
    store_name: str,
    item: str,
    distance_km: float
) -> bool:
    """Send email when surplus food matches user preferences"""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print(f"[worker-email] SMTP not configured, skipping email to {recipient_email}")
        return False
    
    try:
        subject = f"🎉 {store_name} has {item}!"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2ecc71;">Surplus food alert!</h2>
                
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Store:</strong> {store_name}</p>
                    <p><strong>Item:</strong> <span style="font-size: 1.2em; color: #e74c3c;">{item.title()}</span></p>
                    <p><strong>Distance:</strong> {distance_km:.1f} km away</p>
                </div>
                
                <p>This item matches your preferences and is within your search radius!</p>
                
                <p style="color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
                    Guardian • Surplus Food Network
                </p>
            </body>
        </html>
        """
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg["To"] = recipient_email
        
        text_body = f"Surplus food alert!\n\nStore: {store_name}\nItem: {item}\nDistance: {distance_km:.1f} km away"
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"[worker-email] Email sent to {recipient_email}: {item} from {store_name}")
        return True
    
    except Exception as e:
        print(f"[worker-email] Failed to send to {recipient_email}: {str(e)}")
        return False
