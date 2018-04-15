import os 
import sys

dir ="/Users/talha/Downloads/VisionxNLTK-v2.0/TestData/"

files = [f for f in os.listdir(dir) if f.endswith('.jpg')]
count = 0

for file in files:
	count=count+1



	filename=file.split('.')[0]

	if os.path.isfile(dir+filename+".gvocr.json")==1:
		print "Image skipped because its already processed"
		continue

	print "Running "+str(count)+" "+file
	command = "python gv-ocr.py "+dir+file
	# print command
	os.system(command)


