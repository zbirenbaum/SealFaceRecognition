import tensorflow as tf
import tensorflow.contrib.slim as slim

class ConvolutionOp:
    def conv_module(self, net, model_layer, reuse = None, scope = None, **kwargs):
        with tf.variable_scope(scope, 'conv', [net], reuse=reuse):
            net = self.convolution(net, model_layer, kernel_size=3,,, scope='transform', xargs=trans_conv_args)
            net = slim.max_pool2d(net, 3, stride=2, padding='SAME')
            shortcut = net
            for i in range(num_res_layers):
                net = convolution(net, num_kernels, kernel_size=1, groups=groups, shuffle=True,
                                stride=1, padding='SAME', scope='res_%d_1'%i, xargs=res_conv_args)
                net = convolution(net, num_kernels, kernel_size=3, groups=groups, shuffle=False,
                                stride=1, padding='SAME', scope='res_%d_2'%i, xargs=res_conv_args)
                #print('| ---- block_%d' % i)
                net = se_module(net)
                net = net + shortcut
                shortcut = net
        return net

    def channel_shuffle(self, name, x, num_groups):
        with tf.variable_scope(name) as scope:
            n, h, w, c = x.shape.as_list()
            x_reshaped = tf.reshape(x, [-1, h, w, num_groups, c // num_groups])
            x_transposed = tf.transpose(x_reshaped, [0, 1, 2, 4, 3])
            output = tf.reshape(x_transposed, [-1, h, w, c])
            return output

def parametric_relu(x):
    num_channels = x.shape[-1].value
    with tf.variable_scope('PRELU'):
        alpha = tf.get_variable('alpha', (1,1,1,num_channels),
                        initializer=tf.constant_initializer(0.0),
                        dtype=tf.float32)
        mask = x>=0
        mask_pos = tf.cast(mask, tf.float32)
        mask_neg = tf.cast(tf.logical_not(mask), tf.float32)
        return mask_pos * x + mask_neg * alpha * x

def se_module(input_net, ratio=16, reuse = None, scope = None):
    with tf.variable_scope(scope, 'SE', [input_net], reuse=reuse):
        h,w,c = tuple([dim.value for dim in input_net.shape[1:4]])
        assert c % ratio == 0
        hidden_units = int(c / ratio)
        squeeze = slim.avg_pool2d(input_net, [h,w], padding='VALID')
        excitation = slim.flatten(squeeze)
        excitation = slim.fully_connected(excitation, hidden_units, scope='se_fc1',
                                weights_initializer=slim.xavier_initializer(), 
                                activation_fn=tf.nn.relu)
        excitation = slim.fully_connected(excitation, c, scope='se_fc2',
                                weights_initializer=slim.xavier_initializer(), 
                                activation_fn=tf.nn.sigmoid)        
        excitation = tf.reshape(excitation, [-1,1,1,c])
        output_net = input_net * excitation

        return output_net

activation = lambda x: tf.keras.layers.PReLU(shared_axes=[1,2]).apply(x)

