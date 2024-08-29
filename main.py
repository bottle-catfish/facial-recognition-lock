#!/usr/bin/env python3

import boto3
import csv

with open('credentials.csv', 'r') as file : 
    next(file)
    reader=list(csv.reader(file))
    
    access_key_id = reader[0][0]
    secret_access_key = reader[0][1]

client = boto3.client('rekognition', region_name='us-west-2',
                                                 aws_access_key_id = access_key_id, aws_secret_access_key=secret_access_key)

photo = 'admin.jpeg'

with open(photo, 'rb') as image_field : 
    source_bytes = image_field.read()

detect_objects = client.detect_labels(Image={'Bytes': source_bytes})
print(detect_objects)