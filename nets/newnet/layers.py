from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import warnings
from tensorflow.contrib.layers.python.layers import initializers

from tensorflow.contrib.layers.python.layers.initializers import xavier_initializer
warnings.simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf
import tensorflow.contrib.slim as slim

class BaseLayer:
    def __init__(self, shape, kernel_size, inputs, padding, name, initializers, stride):

        self.shape = shape
        self.stride = stride
        self.groups = self.shape[2]
        self.num_outputs = self.shape[1]
        self.res_layers = self.shape[0]
        self.padding = padding
        self.kernel_size = kernel_size
        self.inputs = inputs
        self.name = name
        self.scope = self.name
        self.initializers = initializers
        self.kwargs=self.init_full_args()
        return
    
    def get_model_initializers(self):
        return self.initializers
    def get_model_scope(self):
        return self.scope
    def get_model_shape(self):
        return self.shape
    def init_full_args(self):
        dictargs = {
                'kernel_size': self.kernel_size,
                'stride': self.stride,
                'padding': self.padding,
                'scope': self.scope,
                }
        for key in list(self.initializers.keys()):
            dictargs[key] = self.initializers[key]

    def convolution(self):
        kwargs = self.kwargs
        output = slim.conv2d(self.inputs, self.num_outputs, kwargs)
        return output


class TransformLayer(BaseLayer):
    def __init__(self, shape, kernel_size, inputs=None, padding='SAME', stride=3) -> None:
        self.name = 'transform'
        self.args = {
            'weights_initializer': slim.xavier_initializer(),
            'biases_initializer': tf.constant_initializer(0.0)
        }
        super().__init__(shape=shape, kernel_size=kernel_size, inputs=inputs, padding=padding, name=self.name, initializers=self.args, stride=stride)
        return

class ResidualLayer(BaseLayer):
    def __init__(self, shape, kernel_size, inputs=None, padding='SAME', stride=3) -> None:
        self.name = 'residual'
        self.args = {
            'weights_initializer': slim.xavier_initializer(),
            'biases_initializer': tf.constant_initializer(0.0)
        }
        super().__init__(shape=shape, kernel_size=kernel_size, inputs=inputs, padding=padding, name=self.name, initializers=self.args, stride=stride)
        return

class FinalConvolutionLayer(BaseLayer):
    def __init__(self, shape, kernel_size, inputs=None, padding='SAME', stride=3) -> None:
        self.name = 'final'
        self.args = {
            'weights_initializer': slim.xavier_initializer(),
            'biases_initializer': tf.constant_initializer(0.0),
            'activation_fn': None,
            'normalizer_fn': None,
        }
        super().__init__(shape=shape, kernel_size=kernel_size, inputs=inputs, padding=padding, name=self.name, initializers=self.args, stride=stride)
        return

layer = FinalConvolutionLayer(inputs=images, shape=['0', '1024', '1'], kernel_size=3)
print(layer.convolution())
