
import requests
import msal
import os

# Initialize MSAL client
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPES = ['https://graph.microsoft.com/.default']

msal_app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

def get_access_token():
    token_response = msal_app.acquire_token_for_client(scopes=SCOPES)
    return token_response.get('access_token')

def import_txt_files():
    access_token = get_access_token()
    url = 'https://graph.microsoft.com/v1.0/me/drive/root:/data/reports:/children'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json().get('value', [])
        for file in files:
            download_url = file['@microsoft.graph.downloadUrl']
            content = requests.get(download_url).text
            print(f"Imported {file['name']}: {content}")
    else:
        print(f"Failed to fetch files: {response.status_code}")

if __name__ == '__main__':
    import_txt_files()
