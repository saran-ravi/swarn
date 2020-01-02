import numpy as np

inputs = np.array([[0.1899,0],[.28338,0],[.375,0],[.478,0],[0.565,0],[0.6675,0],[0.777,0],[0.87878,0],[.9666,0],[1.0706,0],[1.1978,0],
              [1.2794,0],[1.3762,0],[1.48,0],[1.57,0],[0.1899,11.31],[.26338,14.23],[.3602,15.33],[.4503,15],[.5147,15.15],[0.6,15.61],
              [0.69,15],[0.75,15],[0.8055,15]],dtype=float) # input data
#X = np.array([[0.66750],[0.7770],[0.87878],[.9666],[1.0706],[1.1978],[1.2794],[1.4062],[1.5]],dtype=float) # input data
expected_output = np.array([[0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9],[1],[1.1],[1.2],[1.3],[1.4],[1.5],[1.6],
              [0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9],[1]],dtype=float) # output
# scale units
#X[:,0]=X[:,0]/np.amax(X[:,0]) # scaling input data
expected_output=expected_output/np.amax(expected_output)

lr=0.1
# split data
#X = np.split(xAll, [3])[0] # training data
#xPredicted = np.split(xAll, [3])[1] # testing data

class Neural_Network(object):
  def __init__(self):
  #parameters
    self.inputSize = 2
    self.outputSize = 1
    self.hiddenSize = 3

  #weights
    self.hidden_weights = np.random.randn(self.inputSize, self.hiddenSize) # (3x2) weight matrix from input to hidden layer
    self.hidden_bias =np.random.randn(1,self.hiddenSize)
    self.output_weights = np.random.randn(self.hiddenSize, self.outputSize) # (3x1) weight matrix from hidden to output layer
    self.output_bias = np.random.randn(1,self.outputSize)
  def forward(self, inputs):
    #forward propagation through our network
    self.hidden_layer_activation = np.dot(inputs,self.hidden_weights)
    self.hidden_layer_activation = self.hidden_layer_activation + self.hidden_bias
    self.hidden_layer_output = self.sigmoid(self.hidden_layer_activation)

    self.output_layer_activation = np.dot(self.hidden_layer_output,self.output_weights)
    self.output_layer_activation += self.output_bias
    predicted_output = self.sigmoid(self.output_layer_activation)
    
    return predicted_output

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))

  def sigmoidPrime(self, s):
    #derivative of sigmoid
    return s * (1 - s)

  def backward(self, inputs, expected_output, predicted_output):
    # backward propagate through the network
    self.error = expected_output - predicted_output
    self.d_predicted_output = self.error * self.sigmoidPrime(predicted_output)
  
    self.error_hidden_layer = self.d_predicted_output.dot(self.output_weights.T)
    self.d_hidden_layer = self.error_hidden_layer * self.sigmoidPrime(self.hidden_layer_output)

  #Updating Weights and Biases
    self.output_weights += self.hidden_layer_output.T.dot(self.d_predicted_output) * lr
    self.output_bias += np.sum(self.d_predicted_output,axis=0,keepdims=True) * lr
    self.hidden_weights += inputs.T.dot(self.d_hidden_layer) * lr
    self.hidden_bias += np.sum(self.d_hidden_layer,axis=0,keepdims=True) * lr
    
  def train(self, X, y):
    o = self.forward(X)
    self.backward(X, y, o)

NN = Neural_Network()
for i in range(1000): # trains the NN 1,000 times
  print ("# " + str(i) + "\n")
  print ("Input (scaled): \n" + str(inputs))
  print ("Actual Output: \n" + str(expected_output))
  print ("Predicted Output: \n" + str(NN.forward(inputs)))
  print ("Loss: \n" + str(np.mean((expected_output - NN.forward(inputs))))) # mean sum squared loss
  print ("\n")
  NN.train(inputs, expected_output)

np.savetxt('output_weights.txt',NN.output_weights)
np.savetxt('hidden_weights.txt',NN.hidden_weights)
np.savetxt('output_bias.txt',NN.output_bias)
np.savetxt('hidden_bias.txt',NN.hidden_bias)
inp=[.8789,0]
print(1.6*NN.forward(inp))

