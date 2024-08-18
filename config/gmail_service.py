import os
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

# Almacena las credenciales en un archivo token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def send_email(receiver_email, subject, message_text):
    service = get_gmail_service()
    if not service:
        raise Exception("No se pudo conectar con el servicio de Gmail")

    message = MIMEText(message_text)
    message['to'] = receiver_email
    message['subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    send_message = {
        'raw': encoded_message
    }

    try:
        service.users().messages().send(userId="me", body=send_message).execute()
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise Exception("No se pudo enviar el correo")
