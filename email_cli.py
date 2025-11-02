#!/usr/bin/env python3
import os
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def send_email(to_addr, subject, text_body, html_body=None, attachments=None, env="dev"):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("MAIL_FROM")
    msg["To"] = to_addr
    msg["Subject"] = subject

    # Body container (text + html)
    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(text_body, "plain"))
    if html_body:
        alt_part.attach(MIMEText(html_body, "html"))
    msg.attach(alt_part)

    # Attach files if any
    if attachments:
        for file_path in attachments:
            if not os.path.isfile(file_path):
                print(f"⚠️ Skipped missing attachment: {file_path}")
                continue
            with open(file_path, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)

    # Select SMTP backend
    if env in ["dev", "staging"]:
        smtp_host = os.getenv("MAILPIT_HOST", "localhost")
        smtp_port = int(os.getenv("MAILPIT_PORT", 1025))
    elif env == "prod":
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
    else:
        raise ValueError("Invalid environment: use dev, staging, or prod")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        if env == "prod":
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.send_message(msg)
        print(f"✅ Email sent successfully to {to_addr} ({env})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send email with attachments (Mailpit or AWS SES)")
    parser.add_argument("--env", default="dev", help="Environment: dev, staging, prod")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--text", required=True, help="Plain text body")
    parser.add_argument("--html", help="HTML body (optional)")
    parser.add_argument("--attachments", nargs="*", help="Paths to attachment files")
    args = parser.parse_args()

    send_email(
        args.to,
        args.subject,
        args.text,
        html_body=args.html,
        attachments=args.attachments,
        env=args.env,
    )

