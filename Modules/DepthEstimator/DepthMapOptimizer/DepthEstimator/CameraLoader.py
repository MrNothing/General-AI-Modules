import cv2
from time import sleep

#description Loader template
#type data source
#icon fa fa-sort-numeric-asc

#param int
image_width = 32
#param int
input_size = 1024

self.key = cv2. waitKey(1)
self.webcam = cv2.VideoCapture(0)

print("shape: "+str(self.getNextCameraFrame()))

#This function is called by the trainer to fetch data
#It output two arrays: one for the inputs, and the other for the labels
#Example inputs: x=[[1, 0, 0], [0, 1, 0], ...]
#Example labels: y=[[1, 0], [0, 1], ...]
def getNextCameraFrame(self):
	check, frame = self.webcam.read()
	img_ = cv2.resize(frame,(self.image_width,self.image_width))
	return self.rgb_to_grayscale(img_)

def rgb_to_grayscale(self, img_orig):
	im = []
	for i in range(self.image_width):
		for j in range(self.image_width):
			r, g, b = img_orig[i, j]
			im.append(r/255)
	return im
