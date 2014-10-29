'''
Created on 26 Oct 2014

@author: Jack The Ripper
'''
from tweepy import StreamListener
import json, time, sys
import os


class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.filesize = 0
        self.fprefix = fprefix
        self.filepath=fprefix + '.'+ time.strftime('%Y%m%d-%H%M%S') + '.json'
        self.output  = open(self.filepath, 'w')
        self.delout  = open('delete.txt', 'a')

    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return False

    def on_status(self, status):
        self.output.write(status + "\n")

#         self.counter += 1
        self.filesize = os.path.getsize(self.filepath)
        if self.filesize >= 104857600:
            self.output.close()
            self.filepath= self.fprefix + '.'+ time.strftime('%Y%m%d-%H%M%S') + '.json'
            self.output = open(self.filepath, 'w')
#             self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 