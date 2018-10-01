import os
import json
from datetime import datetime

import requests
import boto3
from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = os.environ.get('account_sid')
# Your Auth Token from twilio.com/console
auth_token  = os.environ.get('auth_token')
client = Client(account_sid, auth_token)

# AWS S3 Resource
s3 = boto3.resource('s3')

# directory
localDirectory = '/tmp/'

# AWS S3 Bucket Name
s3_bucketName = 'testingshirley'

app = Flask(__name__)

def download_files(media_files_list, _from):
    ''' We need to download the files from Twilio using the Media URL. 
        We'll identify the picture using the sending phone number and 
        a time stamp.
    '''
    for media in media_files_list:
        url = media[0]
        now = f"{datetime.now():%Y-%m-%d %H-%M-%S-%f}"
        messageId = str(_from + "-" + now)
        with open(localDirectory + messageId + '.png', 'wb') as f:
            f.write(requests.get(url).content)

def upload_files():
    ''' After we've downloaded the pictures, we'll loop though and upload
        them to AWS S3 bucket.
    '''
    for root, dirs, files in os.walk(localDirectory):
        for filename in files:
            s3.Bucket(s3_bucketName).upload_file(localDirectory + filename, filename)

def checkNumber(_from):
    ''' Make sure the sender is known, read the json
        file of known senders and return the name if
        it is found.
    '''
    with open('whois.json', 'r') as f:
        knownNumbers = json.load(f)
        if _from in knownNumbers["from"]:
            return knownNumbers["from"][_from]
        else:
            return False

@app.route('/')
def healthCheck():
    return 'Hello!\n'

@app.route('/sms', methods=['GET', 'POST'])
def get_details():
    ''' Main logic of the app. Twilio webhook sends to this
        function directly.  We'll pull out the important parts
        of the message and loop though to get all the media URLs. 

        Then we will check the trusted name list, if there is a match
        we'll download the image so we can upload it to S3.  Then we'll
        let the sender know we received the picture.
    '''
    _from = request.values.get("From", None)
    _body = request.values.get("Body", None)
    _messagesid = request.values.get("MessageSid", None)
    num_media = int(request.values.get("NumMedia", 0))

    media_files_list = [(request.values.get("MediaUrl{}".format(i),None),
                    request.values.get("MediaContentType{}".format(i), None))
                        for i in range(0, num_media)]
    
    # See if the sender is in the trusted list
    name = checkNumber(_from)
    if name != False:
        download_files(media_files_list, _from)
        upload_files()

        print("From {} said: {} with this media URL: {}".format(name, _body, media_files_list))

        message = name + ", thanks for the message!"

        resp = MessagingResponse()
        resp.message(message)

        return str(resp)
    else:
        message = _from + ", sorry but you're not on the list!"
        resp = MessagingResponse()
        resp.message(message)

        return str(resp)

if __name__ == "__main__":
    app.run()