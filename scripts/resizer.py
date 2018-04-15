import os
import cv2
from joblib import Parallel, delayed

def sample_process(imn):
	imx = cv2.imread('images/'+ imn)
	imx = cv2.cvtColor(imx, cv2.COLOR_BGR2GRAY)
	imx = cv2.resize(imx, (50, 70))
	cv2.imwrite('resized/'+ imn, imx)
	print('Done: ', imn)

if __name__ == "__main__":
	Parallel(n_jobs=4)(delayed(sample_process)(imn) for imn in os.listdir('images/'))