import io
import os
import sys
import glob
import csv
import cv2
import re
import natsort
import time
import os.path

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud import credentials
from google.cloud.vision import types


credentials = credentials.get_credentials()
vision_client = vision.ImageAnnotatorClient()

def compareDetectionsY(a, b):
    tl1 = a[0]
    tl2 = b[0]

    if tl1.y < tl2.y or abs(tl1.y - tl2.y) < 10:
        return 1
    return -1

def compareDetectionsX(a, b):
    tl1 = a[0]
    tl2 = b[0]

    if tl1.x < tl2.x:
        return 1
    return -1

def detect_documentT(path, target):

    client = vision.ImageAnnotatorClient()

    listDetections = []

    target.write("TL.x,TL.y,BR.x,BR.y,WORD\n")

    """Detects document features in an image."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    imageOpenCV = cv2.imread(path)

    cv2.imwrite(finalOutputImage,imageOpenCV)

    image = types.Image(content=content)
    
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    for page in document.pages:
        for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        wordString = ''
                        for symbol in list(word.symbols):
                            wordString = wordString + symbol.text
                        # print wordString
                        tl = list(word.bounding_box.vertices)[0]
                        br = list(word.bounding_box.vertices)[2]
                        listDetections.append((tl,br,wordString))
                        wordString = wordString.replace("\"", "")
                        
                        #to output word boxes in file
                        # target.write(str(tl.x) + "," + str(tl.y) + "," + str(br.x) + "," + str(br.y) + "," + wordString.encode("utf-8")+"\n")
                        #cv2.rectangle(imageOpenCV,(tl.x, tl.y), (br.x, br.y), (0, 0, 255), 4)
                        

    print "Done with " + str(path)

    listDetections = sorted(listDetections, cmp=compareDetectionsX, key=None, reverse=True)
    listDetections = sorted(listDetections, cmp=compareDetectionsY, key=None, reverse=True)
    combinedDetections = []
    first = True
    temp = []
    for detection in listDetections:
        if first is True:
            temp.append(detection)
            first = False
            continue

        if abs(temp[-1][1].x - detection[0].x) > 100:
            combinedDetections.append(temp)
            temp = []
            temp.append(detection)
        else:
            temp.append(detection)
    if len(temp) != 0:
        combinedDetections.append(temp)

    for detections in combinedDetections:
        lineString = ''
        for detection in detections:
            lineString += detection[2]
            lineString += ' '

        print lineString
        
        cv2.rectangle(imageOpenCV,(detections[0][0].x, detections[0][0].y), (detections[-1][1].x, detections[-1][1].y), (255, 0, 0), 4)
        target.write(str(detections[0][0].x) + "," + str(detections[0][0].y) + "," + str(detections[-1][1].x) + "," + str(detections[-1][1].x) + "," + lineString.encode("utf-8")+"\n")

    
    cv2.imwrite(finalOutputImage,imageOpenCV)

    print "Done with " + str(path)



# relevant_path='/Users/talha/Downloads/VisionxNLTK-v2.0/GV/data/'
relevant_path='/Users/talha/Downloads/VisionxNLTK-v2.0/TestData/'

included_extensions = ['jpg', 'JPG']
file_names = [fn for fn in os.listdir(relevant_path)
              if any(fn.endswith(ext) for ext in included_extensions)]

count = 0

for filename in file_names:
    print "Processing " + str(count) +" "+filename 
    finalInput = relevant_path + '/' + filename
    filename = filename.replace(".jpg", "")
    finalOutput = relevant_path + 'outputs/' + filename + ".csv"
    finalOutputImage = relevant_path + 'images/' + filename + ".jpeg"
    if os.path.isfile(finalOutput)==0:
        target = open(finalOutput, 'w')
        detect_documentT(finalInput, target)
        target.close()
    else:
        print "Image skipped beacause it's been already processed"
    count += 1