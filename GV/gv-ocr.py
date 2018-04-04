

import argparse
import io
import sys

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

    for text in texts:
        ocr_output='\n"{}"'.format(text.description.encode('utf-8'))
        break
    

    lines = ocr_output.split('\n')

detect_text(sys.argv[1])