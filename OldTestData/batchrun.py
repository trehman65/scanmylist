import os 
import sys

files = [f for f in os.listdir('.') if f.endswith('.jpg')]

count=0
for file in files:

	count=count+1
	print count

	filename=file.split('.')[0]
	
	if os.path.exists(filename+'_out_ocrlines_word_wbb.json'):
		print "Skipping "+file 
		continue
	
	command = "bash run-ocr.sh "+filename+ " "+file
	os.system(command)
	# print command

