import time
import tensorflow as tf
import os

#description Predictor script template
#icon fa fa-magic
#MAIN=Run

#param object
_input = None
#param object
_model = None
#param folder
load_path = ""

def Run(self):

	### defining the model ###

	#input
	predictor = tf.placeholder(tf.float32, shape=[None, self._input.input_size], name="x_input")    
	
	#output
	output = self._model.Run(predictor)

	#initialize everything
	instance = AIBlocks.InitModel(load_path=self.load_path)
	Log("Model initialized!")

	#load test data
	while True:
		frame = []
		for i in range(10):
			frame += self._input.getNextCameraFrame()

		prediction = instance.Run(output, feed_dict={predictor: [frame]})[0]

		SendImageData(self.id, frame[0:1024], self._input.image_width, self._input.image_width, "source")
		SendImageData(self.id, prediction, self._input.image_width, self._input.image_width, "depth")

	AIBlocks.CloseInstance(instance)

