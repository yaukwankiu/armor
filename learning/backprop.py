# backprop.py
# to implement backprob for the simple features
# c.f. https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/code/network.py

"""
from armor.learning import backprop as bp

reload(bp)
NN = bp.Network()
NN()


"""
########################
#   imports
import numpy as np

########################
#   sample data
X   = np.random.random(100)
Y   = np.random.random(100)
Z   = np.random.random(100)
W   = (X+Y-Z<0.1)

xyzw = np.random.random(4)
sampleData = [X, Y, Z]

########################
#   functions
def sigmoid(x):
    return 1. / (1+np.exp(-x))

def neuron(weights, data, activationFunction=sigmoid):
    f = activationFunction
    weights = np.array(weights)
    return f((weights*data).sum())


########################
#   classes
class Network:
    def __init__(self, shape=(3,4,4,1)):
        N = len(shape)
        self.layers = []
        self.weights= []
        for s in shape:
            self.layers.append(np.zeros(s))
        for i in range(N-1):
            self.weights.append(np.random.random((shape[i], shape[i+1])))

    def __call__(self, key=None):
        if key:
            returnValue = getattr(self, key)
        else:
            returnValue = {'layers'     : self.layers,
                           'weights'    : self.weights,
                          }
        return returnValue

    def randomise(self):
        N = len(self.layers)
        for i in range(N-1):
            self.weights[i] = np.random.random(self.weights[i].shape)

    def forwardProp(self, data=xyzw, verbose=False):
        n = len(self.layers[0])
        inData  = data[:n]         #single datum
        outData = data[n:] 
        self.layers[0] = inData
        for i in range(1,len(self.layers)):
            data    = self.layers[i-1]
            weights = self.weights[i-1]
            for j in range(len(self.layers[i])):
                self.layers[i][j] = neuron(weights=weights[:,j], data=data)

        outcome = self.layers[-1]
        err     = np.array(outData) - outData
        return {'outcome'   :   outcome,
                'err'       :   err,
                }
        #mapReduce, blablabla


    def backProp(self):
        pass

    def train(self, data):
        pass
        
    def validate(self, data):
        pass
        
    def classify(self, data):
        pass

    def vectorise(self):
        # doesn't quite work because the first argument is fixed as self
        self.forwardProp    = np.vectorize(self.forwardProp)
        self.backProp       = np.vectorize(self.backProp)
