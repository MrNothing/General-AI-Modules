from os import listdir
from os.path import isfile, join
import random as rand
from PIL import Image
import numpy as np

#description Loader template
#type data source
#icon fa fa-sort-numeric-asc

#param int
image_width = 64
#param int
input_size = 10
#param int
labels_size = 2
#param int
batch_size = 100
#param folder
rgb_folder = ""
#param folder
depth_folder = ""

self.onlyfiles = [f for f in listdir(self.rgb_folder) if not isfile(join(self.rgb_folder, f))]

Log("rgb files: "+str(len(self.onlyfiles)))

#This function is called by the trainer to fetch data
#It output two arrays: one for the inputs, and the other for the labels
#Example inputs: x=[[1, 0, 0], [0, 1, 0], ...]
#Example labels: y=[[1, 0], [0, 1], ...]
def getNextBatch(self):
	x = []
	y = []
	#TODO: fetch some data here...

	for i in range(self.batch_size):
		index = self.getRandomIndex()
		data = []

		for i in range(10):
			data += self.image_file_to_tensor(self.rgb_folder+"/"+self.onlyfiles[index]+"/sc_"+str(i)+".png")

		x.append(data)
		y.append(self.image_file_to_tensor(self.depth_folder+"/"+self.onlyfiles[index]+"/sc_9.png"))

	return x, y

#same rules as 'getNextBatch' except this is from the test dataset
def getTestBatch(self):
	x = []
	y = []
	#TODO: fetch some test data here...

	return x, y

def getRandomIndex(self):
	return rand.randint(0, len(self.onlyfiles)-1)

def image_file_to_tensor(self, path):
	imgpil = Image.open(path)  
	# anciennement np.asarray
	img = np.array(imgpil.getdata()).reshape(imgpil.size[0], imgpil.size[1], 3)
	return self.rgb_to_grayscale(img)

def rgb_to_grayscale(self, img_orig):
	r_im = np.copy(img_orig) # On fait une copie de l'original
	im = []
	for i in range(self.image_width):
		for j in range(self.image_width):
			r, g, b = r_im[i, j]
			im.append(r/255)
	return im
