import numpy as np
import pickle


class TolNet():

    instance_counter = 0

    def __init__(self):
        self.layers = []
        self.activations = []
        self.instance_id = TolNet.instance_counter
        TolNet.instance_counter += 1
        

    #  activation R: relu
    #  activation L: linear (no activation function)
    def addLayer(self, in_size=None, out_size=128, activation="R"):
        assert not (in_size == None and len(self.layers) == 0), "You must give in_size for the first layer!"
        if in_size == None:
            in_size = len(self.layers[-1][1])

        weight = np.random.normal(loc=0, scale=np.sqrt(2/(in_size)), size=(in_size, out_size))
        bias = np.zeros(out_size)
        self.layers.append([weight, bias])
        self.activations.append(activation)
    
    def run(self, input):
        if len(input.shape) == 1:
            input = np.expand_dims(input, 0)

        for i, (weight, bias) in enumerate(self.layers):
            logit = np.dot(input, weight) + bias
            if i != len(self.layers) - 1:
                input = np.maximum(logit, 0)

        if logit.shape[0] == 1:
            logit = logit.squeeze(0)

        return logit

    def __repr__(self):

        string = "\n"
        string += ("-"*15 + " Network " + "-"*16 + "\n")
        for i, (weight, bias) in enumerate(self.layers):
            in_size, out_size = weight.shape
            string += (" Layer {}".format(i) + "\n")
            string += (" Input size: {}".format(in_size) + "\n")
            string += (" Output size: {}".format(out_size) + "\n")
            string += (" Number of parameters: {}".format((in_size + 1)*out_size) + "\n")
            string += ("-"*40 + "\n")
        return string

    def save(self, filename):
        with open(filename, "wb") as dosya:
            pickle.dump((self.layers, id(self), self.instance_id), dosya)

        #pickle.dump(self.layers, open(filename, "wb"))

    def load(self, filename):
        with open(filename, "rb") as dosya:
            self.layers, obj_id, ic = pickle.load(dosya)
        
        #self.layers = pickle.load(open(filename, "rb"))


    """
    Returns a list of numpy array (each element of list is a numpy array)
    ith numpy array represents parameters of the ith layer of the neural network 
    """
    def parameters(self):
        return [np.concatenate([weight.reshape(-1), bias]) for weight, bias in self.layers]

    def update(self, parameters):

        for param, (weight, bias) in zip(parameters, self.layers):
            in_size, out_size = weight.shape
            weight = param[:in_size*out_size].reshape(in_size, out_size)
            bias = param[in_size*out_size:]
        

if __name__ == "__main__":
    input = np.random.normal(size=(1, 50))
    net = TolNet()
    net.addLayer(in_size=50, out_size=64)
    net.addLayer()
    net.addLayer(out_size=4)
    net.save("deleteme")

    param = net.parameters()
    net.update(param)

    output = net.run(input)
    print(net)
