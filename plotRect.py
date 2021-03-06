import cv2 
import json
from pprint import pprint
import numpy as np
import sys
import os

print('test')

abspath=sys.argv[2]

inputImage = sys.argv[1]
filename=inputImage.split('.')[0]

inputJson = abspath+filename+"_nltk.json"
outputImage = abspath+filename+".out.png"


inputImage = abspath+inputImage
img = cv2.imread(inputImage,cv2.IMREAD_COLOR)

overlay = img.copy()
output = img.copy()

alpha = 0.5


with open(inputJson) as data_file:    
    data = json.load(data_file)

lines=data['ie_result']['lines']

for line in lines:

	if line['Label']== 1:
		qty = line['Quantity']

		tags = line['TagsBoxes']
		# print line['product']
		for tag in tags:
			box = tag['tag_bounding_box']

			# t = int(box['top'])*300/1440
			# l = int(box['left'])*300/1440
			# b = int(box['bottom'])*300/1440
			# r = int(box['right'])*300/1440
			
			t = int(box['top'])
			l = int(box['left'])
			b = int(box['bottom'])
			r = int(box['right'])
			
			cv2.rectangle(overlay,(l,t),(r,b),(255,0,0),-1)

		
		words = line['ItemBoxes']
		# print line['product']
		for word in words:
			box = word['word_bounding_box']

			# t = int(box['top'])*300/1440
			# l = int(box['left'])*300/1440
			# b = int(box['bottom'])*300/1440
			# r = int(box['right'])*300/1440
			
			t = int(box['top'])
			l = int(box['left'])
			b = int(box['bottom'])
			r = int(box['right'])
			
			cv2.rectangle(overlay,(l,t),(r,b),(0,255,0),-1)
		


		qty="QTY: "+qty
		cv2.putText(output, qty,(r, b), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),6)			
			

cv2.addWeighted(overlay, alpha, output, 1 - alpha,
		0, output)


cv2.imwrite(outputImage,output)
