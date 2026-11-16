import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from flask import current_app

class EmailService:
    @staticmethod
    def send_otp_email(recipient_email: str, otp_code: str, purpose: str = 'registration', user_name: str = '') -> dict:
        """
        Sends a 6-digit OTP email using SMTP (e.g., Gmail SMTP with App Password).
        If SMTP is unconfigured or in local dev mode, logs the OTP cleanly to the console
        and records it in database/dev_otp_inbox.json so local developers are never blocked.
        """
        config = current_app.config
        smtp_server = config.get('SMTP_SERVER')
        smtp_port = config.get('SMTP_PORT', 587)
        smtp_user = config.get('SMTP_USERNAME', '')
        smtp_pass = config.get('SMTP_PASSWORD', '')
        smtp_use_tls = config.get('SMTP_USE_TLS', True)
        sender_email = config.get('MAIL_DEFAULT_SENDER', 'Secure Auth <noreply@secureportal.com>')
        dev_mode = config.get('DEV_MODE_MOCK_EMAIL', True)

        subject = "Account Verification Code" if purpose == 'registration' else "Password Reset Verification Code"
        greeting_name = user_name if user_name else recipient_email.split('@')[0]
        
        # HTML Email Body
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 24px; }}
            .container {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; padding: 36px 32px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }}
            .logo {{ display: inline-block; font-size: 20px; font-weight: 800; background: linear-gradient(135deg, #2563eb, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }}
            .title {{ font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 12px; }}
            .text {{ font-size: 14px; color: #475569; line-height: 1.6; margin-bottom: 24px; }}
            .otp-box {{ background: #f1f5f9; border: 2px dashed #93c5fd; border-radius: 16px; padding: 20px; text-align: center; margin: 28px 0; }}
            .otp-code {{ font-family: 'Courier New', Courier, monospace; font-size: 38px; font-weight: 800; letter-spacing: 10px; color: #1d4ed8; }}
            .expiry-note {{ font-size: 12px; color: #64748b; margin-top: 8px; font-weight: 600; }}
            .warning {{ font-size: 12px; color: #dc2626; background: #fef2f2; border: 1px solid #fee2e2; border-radius: 10px; padding: 12px; margin-top: 24px; line-height: 1.5; }}
            .footer {{ font-size: 12px; color: #94a3b8; text-align: center; margin-top: 32px; border-top: 1px solid #f1f5f9; padding-top: 20px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="logo">Secure Authentication Portal</div>
            <div class="title">Verify Your Email Address</div>
            <div class="text">
              Hello <strong>{greeting_name}</strong>,<br><br>
              Thank you for registering. Please enter the 6-digit one-time password (OTP) below to complete your {purpose.replace('_', ' ')}.
            </div>
            
            <div class="otp-box">
              <div class="otp-code">{otp_code}</div>
              <div class="expiry-note">⏱️ Valid for 5 minutes only (Single Use)</div>
            </div>

            <div class="warning">
              <strong>Security Alert:</strong> Never share this OTP with anyone. Our administrators and support staff will never ask for your verification code.
            </div>

            <div class="footer">
              This is an automated security email. If you did not request this verification, please safely ignore this message.
            </div>
          </div>
        </body>
        </html>
        """

        # Plaintext alternative
        text_content = f"Hello {greeting_name},\n\nYour 6-digit verification code is: {otp_code}\n\nThis OTP is valid for 5 minutes. Do not share it with anyone."

        # Check if real SMTP credentials are provided
        smtp_success = False
        if smtp_user and smtp_pass and not dev_mode:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = recipient_email
                
                msg.attach(MIMEText(text_content, 'plain'))
                msg.attach(MIMEText(html_content, 'html'))
                
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
                if smtp_use_tls:
                    server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender_email, [recipient_email], msg.as_string())
                server.quit()
                smtp_success = True
                print(f"[EmailService] Real SMTP sent OTP to {recipient_email}")
            except Exception as e:
                print(f"[EmailService Warning] SMTP sending failed: {str(e)}. Falling back to Dev Mode logging.")
                smtp_success = False

        now_utc = datetime.now(timezone.utc)
        print("\n" + "=" * 65)
        print(f" [EMAIL OTP DISPATCH] -> {recipient_email}")
        print(f" Purpose: {purpose.upper()}")
        print(f" >>> ONE-TIME VERIFICATION CODE: {otp_code} <<<")
        print(f" Valid for: 5 Minutes (Expires at {now_utc.strftime('%H:%M:%S UTC')})")
        print("=" * 65 + "\n")

        # Record in dev inbox
        try:
            database_dir = current_app.config.get('DATABASE_DIR')
            if not database_dir:
                database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'database'))
            os.makedirs(database_dir, exist_ok=True)
            inbox_path = os.path.join(database_dir, 'dev_otp_inbox.json')
            inbox = []
            if os.path.exists(inbox_path):
                try:
                    with open(inbox_path, 'r', encoding='utf-8') as f:
                        inbox = json.load(f)
                except Exception:
                    inbox = []
            
            inbox.insert(0, {
                'email': recipient_email,
                'otp_code': otp_code,
                'purpose': purpose,
                'timestamp': now_utc.isoformat()
            })
            # Keep last 50 entries
            inbox = inbox[:50]
            with open(inbox_path, 'w', encoding='utf-8') as f:
                json.dump(inbox, f, indent=2)
        except Exception as e:
            print(f"[EmailService] Failed to record in dev inbox: {e}")

        return {
            'success': True,
            'smtp_delivered': smtp_success,
            'dev_otp': otp_code if dev_mode or not smtp_success else None
        }
