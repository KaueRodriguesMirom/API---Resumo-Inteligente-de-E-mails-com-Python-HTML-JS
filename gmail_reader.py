from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def autenticar_gmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def ler_emails(service, maxResults=5):
    results = service.users().messages().list(userId='me', maxResults=maxResults).execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_id = msg['id']
        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        headers = message.get('payload', {}).get('headers', [])
        snippet = message.get('snippet', 'Resumo não disponível')

        remetente = "Remetente não encontrado"
        data_envio = "Data não encontrada"

        for header in headers:
            if header['name'].lower() == 'from':
                remetente = header['value']
            elif header['name'].lower() == 'date':
                data_envio = header['value']

        emails.append({
            'id': msg_id,
            'from': remetente,
            'date': data_envio,
            'snippet': snippet
        })

    return emails
