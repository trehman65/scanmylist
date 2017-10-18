import os 
import sys

files = [f for f in os.listdir('.') if f.endswith('.jpg')]

for file in files:
	print "Running "+file
	filename=file.split('.')[0]
	command = "bash run.sh "+filename+ " "+file
	os.system(command)
	# print command

