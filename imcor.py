import os
import cv2
import time
from joblib import Parallel, delayed

files = os.listdir('resized/')

def sample_process(input_name, input_image, test_file_id):
	ima = input_image
	imn = input_name
	imm = files[test_file_id]
	im2 = 'resized/' + imm
	#print('\tTest Image: ', imm)
	imb = cv2.imread(im2)
	imx = cv2.matchTemplate(ima, imb, cv2.TM_CCOEFF_NORMED)
	#if imx[0,0] > 0.9:
	#	print('\t\tTemplate Matching Result: ', imx[0,0])
	return ' '.join([imn, imm, str(imx[0,0])])

def main():
	cor_res = open('cor.txt', 'w')
	for i in range(len(files)):
		imn = files[i]
		im1 = 'resized/' + imn
		print('Input Image: "',imn)
		ima = cv2.imread(im1)
		tmp = time.time()
		out = Parallel(n_jobs=6)(delayed(sample_process)(imn, ima, imid) for imid in range(i+1, len(files)))
		print('Time Taken (in seconds): ', time.time()-tmp)
		cor_res.write('\n'.join(out))

	cor_res.close()

if __name__ == "__main__":
	main()