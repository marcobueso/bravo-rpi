    
import datetime
import threading
from time import sleep

from google.cloud import firestore

import os

print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

db = firestore.Client()
# [START listen_for_changes]

# Create an Event for notifying main thread.
delete_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    print(u'Callback received query snapshot.')
    print(u'Current cities in California: ')
    for change in changes:
        if change.type.name == 'ADDED':
            print(u'New city: {}'.format(change.document.id))
        elif change.type.name == 'MODIFIED':
            print(u'Modified city: {}'.format(change.document.id))
        elif change.type.name == 'REMOVED':
            print(u'Removed city: {}'.format(change.document.id))
            delete_done.set()

col_query = db.collection(u'cities').where(u'state', u'==', u'CA')

# Watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)