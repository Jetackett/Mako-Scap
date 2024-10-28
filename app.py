
from flask import Flask, jsonify
import requests
import msal
import os

app = Flask(__name__)

# Read Microsoft Graph API credentials from environment variables
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPES = ['https://graph.microsoft.com/.default']

# MSAL Client Initialization
msal_app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

def get_access_token():
    token_response = msal_app.acquire_token_for_client(scopes=SCOPES)
    return token_response.get('access_token')

@app.route('/reports', methods=['GET'])
def get_reports():
    access_token = get_access_token()
    url = 'https://graph.microsoft.com/v1.0/me/drive/root:/data/reports:/children'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        reports = response.json().get('value', [])
        return jsonify(reports)
    else:
        return jsonify({'error': 'Failed to fetch reports'}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
