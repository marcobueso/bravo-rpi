    
import datetime
import threading
from time import sleep

from google.cloud import firestore

import os
print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/bravo/google-creds.json"
db = firestore.Client()
# [START listen_for_changes]
print('GOT HERE')
# Create an Event for notifying main thread.
delete_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    print(u'Callback received query snapshot.')
    for change in changes:
        if change.type.name == 'ADDED':
            print(u'New message received\n ID: {}'.format(change.document.id))
            print(u'MESSAGE: {}'.format(change.document.get('original')))
        elif change.type.name == 'MODIFIED':
            print(u'Modified city: {}'.format(change.document.id))
        elif change.type.name == 'REMOVED':
            print(u'Removed city: {}'.format(change.document.id))
            delete_done.set()

####col_query = db.collection(u'cities').where(u'state', u'==', u'CA')
col_query = db.collection(u'messages')
# Watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)

while True:
    sleep(1)
    print('processing...')