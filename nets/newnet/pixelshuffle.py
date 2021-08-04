from NumPyNet.layers.shuffler_layer import Shuffler_layer

import numpy as np # the library is entirely based on numpy

batch       = 5
width       = 100
height      = 100
channels_in = 9    # out channels will be channels_in // scale**2, channels in must be an high number

# input definition, the combination of arange, reshape and trasposition offers a nice visualization, but any (batch, width, height, channels) array is ok
input = np.arange(0, batch * width * height * channels_in).reshape(batch, channels_in, width, height)
input = input.transpose(0, 2, 3, 1)

scale = 3

# layer initialization
layer = Shuffler_layer(scale=scale)

# layer forward
layer.backward(delta=delta)

# now delta is updated, to check that everything is fine:

output = layer.output

# layer backward
delta = np.ones(shape=inpt.shape)

def forward(self, inpt):
	'''
	Forward function of the shuffler layer: it recieves as input an image in
	the format ('batch' not yet , in_w, in_h, in_c) and it produce an output
	with shape ('batch', in_w * scale, in_h * scale, in_c // scale**2)

	Parameters:
		inpt : input batch of images to be reorganized, with format (batch, in_w, in_h, in_c)
	'''
	self.batch, self.w, self.h, self.c = inpt.shape

	channel_output = self.c // self.scale_step # out_c

	# The function phase shift receives only in_c // out_c channels at a time
	# the concatenate stitches together every output of the function.

	self.output = np.concatenate([self._phase_shift(inpt[:, :, :, range(i, self.c, channel_output)], self.scale)
																for i in range(channel_output)], axis=3)

	# output shape = (batch, in_w * scale, in_h * scale, in_c // scale**2)
	self.delta = np.zeros(shape=self.out_shape, dtype=float)
