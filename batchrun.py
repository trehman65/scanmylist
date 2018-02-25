import os 
import sys

dir ="/Users/talha/Downloads/VisionxNLTK-v2.0/TestData/"

files = [f for f in os.listdir(dir) if f.endswith('.jpg')]

for file in files:
	print "Running "+file
	filename=file.split('.')[0]
	command = "bash run-nltk-v2.sh "+filename+ " "+file+" "+dir
	os.system(command)

