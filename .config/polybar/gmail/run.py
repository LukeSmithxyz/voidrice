#!/usr/bin/env python

import os
import subprocess
import argparse
import time
import pathlib
from apiclient import discovery, errors
from httplib2 import ServerNotFoundError
from oauth2client import client, file

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--badge', default='\uf0e0')
parser.add_argument('-c', '--color', default='#ff69b4')
parser.add_argument('-m', '--mute', action='store_true')
args = parser.parse_args()

dir = os.path.dirname(os.path.realpath(__file__))
credentials = os.path.join(dir, 'mycredentials.json')
unread_badge = '%{F' + args.color + '}' + args.badge + ' %{F-}'
error_badge = '%{F' + args.color + '}\uf06a %{F-}'
count_was = 0

def update(count_was):
    gmail = discovery.build('gmail', 'v1', credentials=file.Storage(credentials).get())
    labels = gmail.users().labels().get(userId='me', id='INBOX').execute()
    count = labels['messagesUnread']
    if count > 0:
        print(unread_badge + str(count), flush=True)
    else:
        print(args.badge, flush=True)
    if not args.mute and count_was < count and count > 0:
        subprocess.run(['canberra-gtk-play', '-f', '/home/z/bin/music4scripts/tora-yara.ogg'])
    return count

while True:
    try:
        if pathlib.Path(credentials).is_file():
            count_was = update(count_was)
            time.sleep(10)
        else:
            print(error_badge + 'credentials not found', flush=True)
            time.sleep(2)
    except (errors.HttpError, ServerNotFoundError, OSError) as error:
        print(error_badge + str(error), flush=True)
        time.sleep(5)
    except client.AccessTokenRefreshError:
        print(error_badge + 'revoked credentials', flush=True)
        time.sleep(5)



