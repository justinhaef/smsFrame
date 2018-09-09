from flask import Flask, request

import requests
import os

import boto3

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

import uuid # don't use this, use datetime instead.
from datetime import datetime

import instance.config as config

# ToDo -> create a list of known people that are only allowed to send MMS.

# Your Account SID from twilio.com/console
account_sid = config.account_sid
# Your Auth Token from twilio.com/console
auth_token  = config.auth_token

s3 = boto3.resource('s3')

client = Client(account_sid, auth_token)
app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def get_details():
    _from = request.values.get("From", None)
    _body = request.values.get("Body", None)
    _messagesid = request.values.get("MessageSid", None)
    num_media = int(request.values.get("NumMedia", 0))

    media_files_list = [(request.values.get("MediaUrl{}".format(i),None),
                    request.values.get("MediaContentType{}".format(i), None))
                        for i in range(0, num_media)]
    
    download_files(media_files_list)
    upload_files()

    print("From {} said: {} with this media URL: {}".format(_from, _body, media_files_list))

    message = _from + ", thanks for the message!"

    resp = MessagingResponse()
    resp.message(message)

    return str(resp)

def download_files(media_files_list):
    for media in media_files_list:
        url = media[0]
        messageId = str(uuid.uuid4())
        with open('/Users/justinhaefner/Desktop/Shirley/' + messageId + '.png', 'wb') as f:
            f.write(requests.get(url).content)

def upload_files():
    directory = '/Users/justinhaefner/Desktop/Shirley/'
    for root, dirs, files in os.walk(directory):
        for filename in files:
            s3.Bucket('testingshirley').upload_file(directory + filename, filename)

if __name__ == "__main__":
    app.run()