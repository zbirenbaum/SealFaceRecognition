import tensorflow as tf

def get_batch_params(last=False):
    if(last): 
        batch_norm_params = {
            'decay': 0.995,             # Decay for the moving averages.
            'epsilon': 10e-8,           # epsilon to prevent 0s in variance.
            'center': False,            # force in-place updates of mean and variance estimates
            'scale': False,             # not use beta
            'updates_collections': None,# not use gamma
            'variables_collections': [ 
               tf.GraphKeys.TRAINABLE_VARIABLES # Moving averages ends up in the trainable variables collection
            ],
        }
    else:
        batch_norm_params = {
            'decay': 0.995,             # Decay for the moving averages.
            'epsilon': 0.001,           # epsilon to prevent 0s in variance.
            'updates_collections': None,# force in-place updates of mean and variance estimates
            'variables_collections': [ 
                tf.GraphKeys.TRAINABLE_VARIABLES # Moving averages ends up in the trainable variables collection
            ],         
        }
    return batch_norm_params

"""
axis:
    Integer, the axis that should be normalized (typically the features axis).
    For instance, after a Conv2D layer with data_format="channels_first", set axis=1 in BatchNormalization.
momentum:
    Momentum for the moving average.
epsilon:
    Small float added to variance to avoid dividing by zero.
center:
    If True, add offset of beta to normalized tensor. If False, beta is ignored.
scale:
    If True, multiply by gamma. If False, gamma is not used.
    When the next layer is linear (also e.g. nn.relu), this can be disabled since the scaling will be done by the next layer.
beta_initializer:
    Initializer for the beta weight.
gamma_initializer:
    Initializer for the gamma weight.
moving_mean_initializer:
    Initializer for the moving mean.
moving_variance_initializer:
    Initializer for the moving variance.
beta_regularizer:
    Optional regularizer for the beta weight.
gamma_regularizer:
    Optional regularizer for the gamma weight.
beta_constraint:
    Optional constraint for the beta weight.
gamma_constraint:
    Optional constraint for the gamma weight.
"""
