import numpy as np


def sigmoid(s):
    # activation function
    return 1/(1+np.exp(-s))

def sigmoidPrime(s):
    #derivative of sigmoid
    return s * (1 - s)

hidden_weights = np.loadtxt('hidden_weights.txt')
hidden_bias = np.loadtxt('hidden_bias.txt')
output_weights = np.loadtxt('output_weights.txt')
output_bias = np.loadtxt('output_bias.txt')

def forward(inputs):
    #forward propagation through our network
    hidden_layer_activation = np.dot(inputs,hidden_weights)
    hidden_layer_activation = hidden_layer_activation + hidden_bias
    hidden_layer_output = sigmoid(hidden_layer_activation)

    output_layer_activation = np.dot(hidden_layer_output,output_weights)
    output_layer_activation += output_bias
    predicted_output = sigmoid(output_layer_activation)
    
    return predicted_output


inp=[.8789,0]
print(1.6*forward(inp))