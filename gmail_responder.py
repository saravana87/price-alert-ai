import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

from index_loader import load_query_engine

# Gmail scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

import os
api_key = os.getenv("OPENAI_API_KEY")


def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_reply(service, to_email, thread_id, original_subject, reply_text):
    message = MIMEText(reply_text)
    message['To'] = to_email
    message['Subject'] = "Re: " + original_subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {
        'raw': raw,
        'threadId': thread_id
    }

    message = service.users().messages().send(userId='me', body=body).execute()
    print(f"✅ Replied to: {to_email}")

if __name__ == '__main__':
    service = gmail_authenticate()
    query_engine = load_query_engine()
    print("✅ Query engine loaded with OpenAI embedding")

    # Search for user replies
    query = 'subject:"Re: Price Update" is:unread'
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_id = msg['id']
        full = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        thread_id = full.get('threadId')

        headers = full.get('payload', {}).get('headers', [])
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), None)
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "Price Update")

        # Extract plain text body
        body = ""
        parts = full['payload'].get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode()

        print(f"\n📨 From: {from_email}\n✉️ Message: {body.strip()}")
        print("QUERYING:", body.strip())

        # Get AI response from LlamaIndex
        response = query_engine.query(body.strip())

        # Send reply
        send_reply(service, from_email, thread_id, subject, str(response))
