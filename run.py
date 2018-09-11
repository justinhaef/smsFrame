import requests
import os
import json
from datetime import datetime

import boto3
from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

import instance.config as config

# Your Account SID from twilio.com/console
account_sid = config.account_sid
# Your Auth Token from twilio.com/console
auth_token  = config.auth_token
client = Client(account_sid, auth_token)

# AWS S3 Resource
s3 = boto3.resource('s3')

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

def download_files(media_files_list, _from):
    for media in media_files_list:
        url = media[0]
        now = f"{datetime.now():%Y-%m-%d %H-%M-%S-%f}"
        messageId = str(_from + "-" + now)
        with open('/Users/justinhaefner/Desktop/Shirley/' + messageId + '.png', 'wb') as f:
            f.write(requests.get(url).content)

def upload_files():
    directory = '/Users/justinhaefner/Desktop/Shirley/'
    for root, dirs, files in os.walk(directory):
        for filename in files:
            s3.Bucket('testingshirley').upload_file(directory + filename, filename)

def checkNumber(_from):
    with open('whois.json', 'r') as f:
        knownNumbers = json.load(f)
        if _from in knownNumbers["from"]:
            return knownNumbers["from"][_from]
        else:
            return False

if __name__ == "__main__":
    app.run()