import os
import time
import shutil

start = time.time()
for fn in os.listdir('images/'):
	shutil.copy('images/'+fn, 'unique/')
print('Time to copy: ', time.time()-start)

total_files = len(os.listdir('images/'))
removed = 0

with open('cor.txt') as f:
	lines = [ln.strip() for ln in f.readlines()]
	for ln in lines:
		arg = ln.split(' ')
		f1 = arg[0]
		f2 = arg[1]
		if len(arg)!=3:
			cr1 = float(arg[2][:-8])
			if cr1>0.8 and os.path.isfile('unique/'+f2):
				os.remove('unique/'+f2)
				print('Deleting file:',f2,'with confidence',cr1)
				removed +=1
			f1 = arg[2][-8:]
			f2 = arg[3]
			cr = float(arg[4])
		else:
			cr = float(arg[2])
		if cr>0.8 and os.path.isfile('unique/'+f2):
			os.remove('unique/'+f2)
			print('Deleting file:',f2,'with confidence',cr)
			removed+=1

print('Duplication: ', 100*removed/total_files,'%')
