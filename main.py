#!/usr/bin/env python3

import boto3
import csv
import base64

#Getting aws keys
with open('credentials.csv', 'r') as file : 
    next(file)
    reader=list(csv.reader(file))
    
    access_key_id = reader[0][0]
    secret_access_key = reader[0][1]

#Setting up the client
client = boto3.client('rekognition', region_name='us-west-2',
                                                 aws_access_key_id = access_key_id, aws_secret_access_key=secret_access_key)

admin_image = 'Admin.jpg' #This is an admin and should be considered acceptable for the lock to actuate
test1_image = 'Test1.jpg' #Test Case 1

admin_bytes = open(admin_image, 'rb')
test1_bytes = open(test1_image, 'rb')



response=client.compare_faces(SimilarityThreshold=70,
                                  SourceImage={'Bytes': admin_bytes.read()},
                                  TargetImage={'Bytes': test1_bytes.read()})

# detect_objects = client.detect_labels(Image={'Bytes': admin_bytes})

print(response)