

import argparse
import io
import sys
import json

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

    data={}
    data["sentences"]=[]

    for text in texts:
        ocr_output='\n"{}"'.format(text.description.encode('utf-8'))
        break
    


    lines = ocr_output.split('\n')
    count=0
    for line in lines:
        thisline={}
        thisline["sentenceID"]=count
        thisline["sentence"]=line
        thisline["words"]=[]
        words=line.split(' ')
        
        for word in words:
            thisword={}
            thisword["word"]=word
            thisword["boundingbox"]={"top":'',"left":'',"bottom":'',"right":'',}
            thisline["words"].append(thisword)


        data["sentences"].append(thisline)
        count=count+1
    
    json.dump(data, open('ocr.json', 'wb'))


detect_text(sys.argv[1])