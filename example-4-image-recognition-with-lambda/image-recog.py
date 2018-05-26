from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

print('Loading function')

rekognition = boto3.client('rekognition')
client = boto3.client('sns')

def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    
    return response


# --------------- Main handler ------------------

def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    
    print (event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        

        # Calls rekognition DetectLabels API to detect labels in S3 object
        response = detect_labels(bucket, key)
        
        tosend=""
        
        for Label in response["Labels"]:
           # print (Label["Name"] + Label["Confidence"])
            
            print ('{0} - {1}%'.format(Label["Name"], Label["Confidence"]))
            tosend+= '{0} - {1}% '.format(Label["Name"], Label["Confidence"])
            
        
        message = client.publish(TargetArn='arn:aws:sns:us-east-1:771452637355:Image-recognition-sns', Message=tosend ,Subject='Uploaded Image Labels')
        
    
        return "hello"
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

