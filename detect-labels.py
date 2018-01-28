from google.cloud import vision
from google.cloud import credentials
import io
from google.cloud.vision import types
import sys

def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels Score')

    for label in labels:
        print label.description +" "+str(label.score)


detect_labels(sys.argv[1])