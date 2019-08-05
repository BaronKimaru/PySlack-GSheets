from pprint import pprint
import argparse
import os
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools


def getCreds():
    service = None
    try:
        scope = "https://www.googleapis.com/auth/spreadsheets"
        client_secrets = os.path.abspath(
            'C:/Users/BaronKimaru/Desktop/credentials.json')
        store = file.Storage('storage.json')
        creds = store.get()
        print("getCreds says creds is present as: ", creds)

        # if not present, create a handshake for its formation
        if not creds or creds.invalid:
            flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()
            pprint(flags)
            flow = client.flow_from_clientsecrets(client_secrets, scope)
            creds = tools.run_flow(flow, store, flags)
            pprint(creds)

        service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

    except Exception as e:
        pprint(e), pprint(type(e))
        pprint("General Error")

    return service
