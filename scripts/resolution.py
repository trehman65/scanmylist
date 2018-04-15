
import os
import sys

files = [f for f in os.listdir('.') if f.endswith('.jpg')]

for file in files:
	command = "convert -units PixelsPerInch "+file +" -density 300 " + file
	print "Processing on "+ file
	os.system(command)