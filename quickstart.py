from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/apps.order']


def main():
    """Calls the Admin SDK Reseller API. Prints the customer ID, SKU ID,
    and plan name of the first 10 subscriptions managed by the domain.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('reseller', 'v1', credentials=creds)

    # Call the Admin SDK Reseller API
    print('Getting the first 10 subscriptions')
    results = service.subscriptions().list(maxResults=10).execute()
    subscriptions = results.get('subscriptions', [])
    if not subscriptions:
        print('No subscriptions found.')
    else:
        print('Subscriptions:')
        for subscription in subscriptions:
            print(u'{0} ({1}, {2})'.format(subscription['customerId'],
                                           subscription['skuId'], subscription['plan']['planName']))


if __name__ == '__main__':
    main()
