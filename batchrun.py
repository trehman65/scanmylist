import os 
import sys

dir ="/Users/talha/Downloads/images/"

files = [f for f in os.listdir('.') if f.endswith('.jpg')]

for file in files:
	print "Running "+file
	filename=file.split('.')[0]
	command = "bash run-nltk-v2.sh "+filename+ " "+file
	os.system(command)
	# print command

