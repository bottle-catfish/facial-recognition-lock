#!/usr/bin/env python3

import boto3, csv, glob, os

#Getting aws keys
with open('credentials.csv', 'r') as file : 
    next(file)
    reader=list(csv.reader(file))
    
    access_key_id = reader[0][0]
    secret_access_key = reader[0][1]

#Setting up the client
client = boto3.client('rekognition', region_name='us-west-2',
                                                 aws_access_key_id = access_key_id, aws_secret_access_key=secret_access_key)


os.chdir("./captures") #Change directory to capture pictures
test_images = [f for f in glob.glob("*jpg")] #Get all the camera captures
if not test_images:
    print("No test images found in ./captures directory.")
    exit()
print(test_images[0])
test1_bytes = open(test_images[0], 'rb') #Assume the first file is the most recent capture and should be used as a check
target_bytes = test1_bytes.read()

os.chdir("../")

os.chdir("./admins") #Change directory to admin pictures
admin_images = [f for f in glob.glob("*jpg")] 
if not admin_images:
    print("No admin images found in ./admins directory.")
    exit()

detection = False
similarity = 0

for i in range(len(admin_images)) : 
    with open(admin_images[i], 'rb') as image_file : 
        source_bytes = image_file.read()
    response = client.compare_faces(SourceImage={'Bytes' : source_bytes}, TargetImage={'Bytes' : target_bytes})
    
    if len(response['FaceMatches']) > 0 and response['FaceMatches'][0]['Similarity'] >= 95 : 
        similarity = response['FaceMatches'][0]['Similarity']
        detection = True

os.chdir("../")

if detection : 
    sim_string = str(round(similarity,2)) + "%"
    print("User recognized with a similarity of :",sim_string)
    print("Unlocking...")
else : 
    print("Unauthorized User. Access Denied...")