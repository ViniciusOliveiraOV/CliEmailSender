import os
import zipfile
import mimetypes
import smtplib
import base64
import keyring

from email.message import EmailMessage
from getpass import getpass

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Scopes for sending Gmail
SCOPES = ['https://mail.google.com/']

def zip_project_folder(folder_path, zip_name="project.zip"):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    return zip_name

def get_gmail_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email_with_attachment(sender, to, subject, body, attachment_path):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            mime_type, _ = mimetypes.guess_type(attachment_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            maintype, subtype = mime_type.split('/', 1)
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=os.path.basename(attachment_path))
    except Exception as e:
        print(f"[!] Error attaching file: {e}")
        return

    try:
        creds = get_gmail_credentials()
        access_token = creds.token

        auth_string = f'user={sender}\1auth=Bearer {access_token}\1\1'
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string.encode()).decode())
        smtp.send_message(msg)
        smtp.quit()
        print("[+] Email sent successfully!")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

if __name__ == "__main__":
    print("📦 Zipping project...")
    folder = input("Enter the project folder path to zip: ").strip()
    zip_file = zip_project_folder(folder)

    sender_email = input("Your Gmail address: ").strip()
    recipient = input("Recipient email: ").strip()
    subject = input("Subject: ").strip()
    body = input("Email body: ").strip()

    send_email_with_attachment(sender_email, recipient, subject, body, zip_file)


