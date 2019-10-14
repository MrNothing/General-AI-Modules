import time
import tensorflow as tf
import os

#description Classifier script template
#icon fa fa-magic
#MAIN=Run

#param object
_input = None
#param object
_model = None
#param float
learning_rate = 0.0001
#param int
training_iterations = 3000	
#param int
display_step = 100
#param folder
save_path = ""

def Run(self):
	test = self._input.getNextBatch()
	#SendImageData(self.id, test[0][0], self._input.image_width, self._input.image_width, "Original")

	### defining the model: ###

	#inputs: 
	self.X = tf.placeholder(tf.float32, shape=[None, self._input.input_size], name="x_input")        
	self.y = tf.placeholder(tf.float32, shape=[None, self._input.labels_size], name="y_labels")
   	
    #	ouput: 
	output = self._model.Run(self.X)

	#Loss function
	_loss = tf.reduce_mean(tf.pow(output-self.y, 2))

	#run the optimizer
	_solver = tf.train.AdamOptimizer(self.learning_rate).minimize(_loss)

	#initalize everything
	instance = AIBlocks.InitModel(load_path=self.save_path)
	Log("Model initialized!")

	#set the progress bar state
	SetState(self.id, 0.001)
        
	for it in range(self.training_iterations):
		batch = self._input.getNextBatch()
            
		X_batch  = batch[0]
		Y_batch  = batch[1]
        
		_, loss = instance.Run([_solver, _loss], feed_dict={self.X: X_batch, self.y: Y_batch})

		#every N steps, send the state to the scene
		if it % self.display_step == 0:
			SetState(self.id, it/self.training_iterations)
			SendChartData(self.id, "Loss", loss, "#ff0000")
			
			test_X = [X_batch[0]]
			test_Y = [Y_batch[0]]
			rebuilt_image = instance.Run(output, feed_dict = {self.X: test_X})[0]
			SendImageData(self.id, test_X[0][0:1024], self._input.image_width, self._input.image_width, "original")
			SendImageData(self.id, test_Y[0], self._input.image_width, self._input.image_width, "depth")
			SendImageData(self.id, rebuilt_image, self._input.image_width, self._input.image_width, "fake")
        
	AIBlocks.SaveModel(instance)
	AIBlocks.CloseInstance(instance)

