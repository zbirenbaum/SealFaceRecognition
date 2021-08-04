from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import tensorflow.contrib.slim as slim

class Parameters:
    def __init__(self):
        self.model_params_dict = {
            'znet': ([0, 1, 2, 1], [64, 256, 512, 1024], [1,32,32,32,32]),
            'znetDropout': ([0,0,0,0], [64,128,256,512], [1,1,1,1,1])
        }
        self.trans_conv_args = {
            'weights_initializer': slim.xavier_initializer(),
            'biases_initializer': tf.constant_initializer(0.0)
        }

        self.res_conv_args = {
            'weights_initializer': tf.truncated_normal_initializer(stddev=0.01),
            'biases_initializer': None
        }

        self.final_convolution_args = {
            'weights_initializer': slim.xavier_initializer(),
            'biases_initializer': tf.constant_initializer(0.0),
            'activation_fn': None,
            'normalizer_fn': None,
        }
        return
    
    def get_model_params(self, model=None):
        if model:
            return self.model_params_dict[model]
        return self.model_params_dict

    def get_fconv_args(self):
        return self.final_convolution_args

    def get_res_conv_args(self):
        return self.res_conv_args

    def get_trans_conv_args(self):
        return self.trans_conv_args
