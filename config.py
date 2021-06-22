''' Config Proto '''

import sys
import os


####### INPUT OUTPUT #######

# me of the current model for output

fold_number = 1

name = 'seal_net_fold_' + str(fold_number)

# The folder to save log and model
log_base_dir = './log/'

# The interval between writing summary
summary_interval = 5

# Cross-validation Parameters
K_CV = 5    # Number of cross-validation folds (training/testing splits)
splits_path = './splits'

#Target image size for the input of network
image_size = [112,112]

# 3 channels means RGB, 1 channel for grayscale
channels = 3

# Resize images before processing, assign as (w,h) or False
resize = (112,112)

# Preprocessing for training
preprocess_train = [
        ('resize', [(112,112)]),
        ('random_flip', []),
        ('standardize', ['deb'])
]

preprocess_test = [
        ('resize', [(112,112)]),
        ('standardize', ['deb'])
]

# Number of GPUs
num_gpus = 1


####### NETWORK #######

# Auto alignment network
localization_net = None

# The network architecture
network = "nets/seal_net.py"

# Model version, only for some networks
model_version = 'seal'

# Number of dimensions in the embedding space
embedding_size = 512


####### TRAINING STRATEGY #######

#The learning rate is a hyperparameter that controls how much to change the model in
#response to the estimated error each time the model weights are updated
#very important hyperparameter

#RMSPROP is a type of stochastic gradient descent with adaptive learning rates
# Optimizer
optimizer = "RMSPROP"

# Number of samples per batch
batch_size = 64

# Number of batches per epoch
epoch_size = 20

# Number of epochs
num_epochs = 30

#learning rate strategy
learning_rate_strategy = 'step'

# learning rate schedule
learning_rate_schedule = {
    0:      0.001,
    #400:      0.01,
    #480:    0.001,
    #5000:   0.001,
    #7000:   0.0001
}

# Multiply the learning rate for variables that contain certain keywords
learning_rate_multipliers = {
    'InceptionResnetV2': 0.000,
}

# Build batches with random templates rather than instances
template_batch = False

# Restore model
restore_model = False

# Keywords to filter restore variables, set None for all
restore_scopes = None

# Weight decay for model variables
weight_decay = 5e-4

# Keep probability for dropouts
# keep_prob value is used to control the dropout rate when training the neural network
# means that each connection between layers will only be used with probability 1 when training
# This reduces overfitting.
keep_prob = 1.0



####### LOSS FUNCTION #######
# Also known as error function, estimates the loss or error of the model so that the weights
# can be updated
# Scale for the logits
losses = {
    #'softmax': {},
    #'cosine': {'gamma': 'auto'},
    #'angular': {'m': 4, 'lamb_min':5.0, 'lamb_max':1500.0},
    # 'split': {'gamma': 'auto'}
     'norm': {'alpha': 1e-5},
}

