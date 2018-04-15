import argparse
import io
import sys
import json
import random
import cv2
import string

from google.cloud import vision

def detect_text(path):

    filename=path.split('/')[-1]
    requestID=filename.split('.')[0]
    abspath=path.replace(filename,'')
    
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    # [START migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    imageOpenCV = cv2.imread(path)

    data={}
    ocr_output=""
    data["sentences"]=[]
    worddata={}
    worddata["words"]=[]

    count=0
    for text in texts:

        if count==0:
            ocr_output='\n"{}"'.format(text.description.encode('utf-8'))
            count=count+1
            continue
        else:
            thisworddata={}

            word='"{}"'.format(text.description.encode('utf-8'))
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
            box={"top":'',"left":'',"bottom":'',"right":'',}
            lefttop= min(vertices)
            rightbottom= max(vertices)

            box["left"]= lefttop.split(',')[0].replace('(','')
            box["top"]= lefttop.split(',')[1].replace(')','')
            box["right"]= rightbottom.split(',')[0].replace('(','')
            box["bottom"]= rightbottom.split(',')[1].replace(')','')
            
            thisworddata["word"]=word
            thisworddata["boundingbox"]=box
            thisworddata["visited"]=0
            worddata["words"].append(thisworddata)
            # cv2.rectangle(imageOpenCV,(int(box["left"]), int(box["top"])), (int(box["right"]), int(box["bottom"])), (255, 0, 0), 4)


        count=count+1
    
    # cv2.imwrite('/Users/talha/Downloads/VisionxNLTK-v2.0/GV/box.png',imageOpenCV)
    # json.dump(worddata, open('words.json', 'wb'))

    ocr_output=ocr_output.replace('\"','')
    lines = ocr_output.split('\n')
    index=0

    for line in lines:
        
        if len(line)==0:
            continue

        # print line
        thisline={}
        thisline["sentenceID"]=index
        thisline["sentence"]=line
        thisline["words"]=[]
        words=line.split(' ')

        r=random.randint(1,255)
        g=random.randint(1,255)
        b=random.randint(1,255)
        
        for word in words:
            word=word.replace("\"",'');
            thisword={}
            thisword["word"]=word
            thisword["boundingbox"]=[]
            ## assign boxes to words by comparison

            for wordinfo in worddata["words"]:
                if wordinfo["visited"]==0 and wordinfo["word"].replace("\"",'').translate(None, string.punctuation)==word.translate(None, string.punctuation):
                    thisword["boundingbox"]=wordinfo["boundingbox"]
                    # box=wordinfo["boundingbox"]
                    # print "Matched"
                    wordinfo["visited"]=1
                    # cv2.rectangle(imageOpenCV,(int(box["left"]), int(box["top"])), (int(box["right"]), int(box["bottom"])), (r, g, b), 4)

                    break

            thisline["words"].append(thisword)


        data["sentences"].append(thisline)
        index=index+1
    
    json.dump(data, open(abspath+requestID+'.gvocr.json', 'wb'))
    return data
    # cv2.imwrite('/Users/talha/Downloads/VisionxNLTK-v2.0/GV/box.png',imageOpenCV)
