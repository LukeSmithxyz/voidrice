#!/usr/bin/env python

import pathlib
import os
import webbrowser
import httplib2
from oauth2client import client, file

target = 'https://www.googleapis.com/auth/gmail.readonly'
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
dir = os.path.dirname(os.path.realpath(__file__))
secrets = os.path.join(dir, 'secrets.json')
credentials = os.path.join(dir, 'mycredentials.json')
storage = file.Storage(credentials)

if pathlib.Path(credentials).is_file():
    credentials = storage.get()
    credentials.refresh(httplib2.Http())
    print("credentials refreshed")
else:
    flow = client.flow_from_clientsecrets(secrets, scope=target,redirect_uri=redirect_uri)
    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    auth_code = input('Enter the auth code: ')
    credentials = flow.step2_exchange(auth_code)
    storage.put(credentials)
    print('Credentials created')

