import boto3
import botocore

from datetime import datetime

import os

localFileList = []
remoteFileList = []

def getLocalFiles(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            localFileList.append(filename)

def getRemoteFiles(bucket):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket)

    for page in page_iterator:
        for item in page['Contents']:
            remoteFileList.append(item['Key'])

def downloadMissingFiles(pictureDirectory, remoteBucket):
    s3 = boto3.resource('s3')

    for file in missingFiles:
        try:
            s3.Bucket(remoteBucket).download_file(file, os.path.join(pictureDirectory, file))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

if __name__ == "__main__":
    pictureDirectory = '/Users/justinhaefner/Desktop/Shirley/'
    s3Bucket = 'testingshirley'
    getLocalFiles(pictureDirectory)
    print("Local filename are {}".format(localFileList))
    getRemoteFiles(s3Bucket)
    print("Remote filenames are {}".format(remoteFileList))
    missingFiles = list(set(remoteFileList).difference(localFileList))
    print("Missing from local are {}".format(missingFiles))
    downloadMissingFiles(pictureDirectory, s3Bucket)
