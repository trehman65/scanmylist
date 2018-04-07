

import argparse
import io
import sys
import json
import cv2


from google.cloud import vision

def detect_text(path):
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
    data["sentences"]=[]
    worddata={}
    worddata["words"]=[]

    count=0
    for text in texts:
        ocr_output='\n"{}"'.format(text.description.encode('utf-8'))
        
        if count==0:
            count=count+1
            continue
        else:
            thisworddata={}

            word='\n"{}"'.format(text.description.encode('utf-8'))
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
    
    json.dump(worddata, open('words.json', 'wb'))

    lines = ocr_output.split('\n')
    index=0
    for line in lines:
        thisline={}
        thisline["sentenceID"]=index
        thisline["sentence"]=line
        thisline["words"]=[]
        words=line.split(' ')
        
        for word in words:
            thisword={}
            thisword["word"]=word

            thisword["boundingbox"]={"top":'',"left":'',"bottom":'',"right":'',}
            thisline["words"].append(thisword)


        data["sentences"].append(thisline)
        index=index+1
    
    json.dump(data, open('ocr.json', 'wb'))


detect_text(sys.argv[1])