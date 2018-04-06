import os 
import sys

dir ="/Users/talha/Downloads/VisionxNLTK-v2.0/TestData/"

files = [f for f in os.listdir(dir) if f.endswith('.jpg')]

for file in files:

	filename=file.split('.')[0]

	if os.path.isfile(dir+filename+"_nltk.json")==1:
		print "Image skipped because its already processed"
		continue

	print "Running "+file
	command = "python nltk_info_ext_gv.py "+file+ " "+filename+" "+dir
	os.system(command)

