from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import tensorflow as tf
import tensorflow.contrib.slim as slim
"""
conv1:
    num_layers=0
    num_kernels=64
    groups=1
conv_2:
    num_layers=1
    num_kernels=256
    groups=32
conv_3:
    num_layers=2
    num_kernels=512
    groups=32
conv_4:
    num_layers=1
    num_kernels=1024
    groups=32
convolution:
    net=?
    bottleneck_layer_size=embed = 512
    kernel_size=?
"""
class NetRun:
    def __init__(self, netarch):
        self.networkobj = netarch
        self.netname = netarch.
def inference(images, keep_probability, phase_train=True, bottleneck_layer_size=512, 
            weight_decay=0.0, reuse=None, model_version=None):
    with slim.arg_scope([slim.conv2d, slim.fully_connected],
                        weights_regularizer=slim.l2_regularizer(weight_decay),
                        activation_fn=activation,
                        normalizer_fn=None,
                        normalizer_params=None):
        with slim.arg_scope(
                            [slim.dropout],
                            keep_prob=keep_probability,
                            is_training=phase_train):
            with tf.variable_scope('SealNet', [images], reuse=reuse):
                with slim.arg_scope([slim.batch_norm, slim.dropout],
                                    is_training=phase_train):
                    print('SealNet input shape:', [dim.value for dim in images.shape])
                    
                    model_version = '4' if model_version ==None else model_version
                    num_layers, num_kernels, groups = model_params[model_version]

                    net = conv_module(images, num_layers[0], num_kernels[0], groups[0], scope='conv1')
                    print('module_1 shape:', [dim.value for dim in net.shape])

                    net = conv_module(net, num_layers[1], num_kernels[1], groups[1], scope='conv2')
                    print('module_2 shape:', [dim.value for dim in net.shape])

                    net = conv_module(net, num_layers[2], num_kernels[2], groups[2], scope='conv3')
                    print('module_3 shape:', [dim.value for dim in net.shape])

                    net = conv_module(net, num_layers[3], num_kernels[3], groups[3], scope='conv4')
                    print('module_4 shape:', [dim.value for dim in net.shape])


def convolution(scope, net, model_layer, **kwargs):
    num_kernels = model_layer.get_num_kernels()
    groups = model_layer.get_num_groups()
    assert num_kernels % groups == 0, '%d %d' % (num_kernels, groups) #WHY MUST THIS BE TRUE?
    if groups==1:
        net = slim.conv2d(net, num_kernels, **kwargs)
        output = slim.dropout(net)
    else:
        with tf.variable_scope(scope, 'group_conv'):
            num_kernels_split = int(num_kernels / groups)
            input_splits = tf.split(net, groups, axis=3)
            output_splits = [
                    slim.conv2d(
                        input_split, 
                        num_kernels_split, 
                        **kwargs
                        ) for input_split in input_splits
                    ]
            output = tf.concat(output_splits, axis=3)
            if kwargs['shuffle']:
                output = channel_shuffle('shuffle', output, groups)
    return output




class Network:
    def __init__(self, model, dropoutmodel=None):
        self.model = Model(model)
        self.dropoutmodel = None 
        if dropoutmodel is not None:
            self.dropoutmodel = Model(model=dropoutmodel, dropoutmodel=True)

        def run_net(self, net):
            for i in range(self.model.num_conv_layers):
                conv_args = self.model.create_conv_parameter('trans')
                net = self.do_convolution(net, self.model.get_layers(i), 'trans')

        def do_convolution(self, net, model_layer, scope):
            print(conv_args)
            net = convolution(net, model_layer, conv_args)
            return net

class ModelLayer():
    def __init__(self, nlayers, nkernels, ngroups):
        self.num_layers = nlayers
        self.num_kernels = nkernels 
        self.groups = ngroups
        return

    def __str__(self):
        return str([self.num_layers, self.num_kernels, self.groups])

class Model:
    def __init__(self, model, dropoutmodel=False):
        self.modelname = model
        self.dropoutmodelname = dropoutmodel
        self.num_conv_layers=0
        self.pobj= Parameters() 
        self.model_params_dict = self.pobj.get_model_params() #
        self.trans_conv_args = self.pobj.get_trans_conv_args()
        self.res_conv_args = self.pobj.get_res_conv_args()
        self.fc_args = self.pobj.get_fconv_args()
        self.conv_layers = []
        self.net = None
        self.model = self.init_model(model)
        self.dropoutmodel = self.init_model(dropoutmodel)
        return

    def get_availiable_models(self):
        return [model for model in self.model_params_dict.keys()]

    def init_model(self, model):
        nlayers, nkernels, ngroups = self.model_params_dict[model]
        assert(len(nlayers) == len(nkernels) == len(ngroups))
        self.num_conv_layers = len(nlayers)
        for i in range(self.num_conv_layers):
            layer = ModelLayer(nlayers[i], nkernels[i], ngroups[i])
            self.conv_layers.append(layer)
        return

    def get_layers(self, index=None):
        if len(self.conv_layers) == 0:
            print("Please init_model(modelname) first")
            exit(1)
        if index is not None:
            return self.conv_layers[index]
        else:
            return self.conv_layers


class Parameters:
    def __init__(self):
        self.model_params_dict = {
            'znet': ([0, 1, 2, 1, None], [64, 256, 512, 1024, None], [1,32,32,32,32]),
            'znetDropout': ([0,0,0,0,None], [64,128,256,512, None], [1,1,1,1,1])
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

        self.conv_defaults = {
                'shuffle': False, 
                'stride': 1,
                'padding': 'SAME',
                'scope': None,
        }
        return

    def get_model_params(self, model=None):
        if model:
            return self.model_params_dict.copy()
        return self.model_params_dict.copy()

    def get_fconv_args(self):
        return self.final_convolution_args.copy()

    def get_res_conv_args(self):
        return self.res_conv_args.copy()

    def get_trans_conv_args(self):
        return self.trans_conv_args.copy()

    def create_conv_parameter(self, conv_type, shuffle=False, stride=1, padding='SAME'):
        param_dict={}
        stringfunc= 'get_{}_conv_args'.format(conv_type)
        param_dict = getattr(self, stringfunc)()
        param_dict['shuffle'] = shuffle
        param_dict['padding'] = padding
        param_dict['stride'] = stride
        param_dict['kernel_size']=3
        return param_dict 
         


test= ZNet()
print(zip(test.model_params_dict['znet']))
test.init_model('znet')
for layer in test.get_layers():
    print(layer)
test.do_convolution(net, test.get_layers(0))
"""
def convolution(net, model_layer, shuffle=False, 
        stride=1, padding='SAME', scope=None, xargs=trans_conv_args):
    assert num_kernels % groups == 0, '%d %d' % (num_kernels, groups)
    if groups==1:
        net = slim.conv2d(net, num_kernels, kernel_size=kernel_size, stride=stride, padding=padding, scope=scope, **xargs)

"""
