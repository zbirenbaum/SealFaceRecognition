import pandas as pd
import numpy as np
import utils
from network import Network
import traintestsplit as ttsplit
from pdb import set_trace as bp

config = utils.import_file('config.py', 'config')
num_trainings = 5
builder = ttsplit.DatasetBuilder(
        photodir='data/fulldataset/2019data',
        usedict=1,
        settype='closed',
        kfold=int(num_trainings)
        )

#print(builder.dsetbyfold[0].set_list)
trainset = builder.dsetbyfold[0]
testset = builder.testsetbyfold[0]
probe_set = builder.probesetbyfold[0]
splits_path = config.splits_path + '/' + config.testing_type + '/fold1/train.txt'.format(1)
trainset = utils.Dataset(path=splits_path)
print(trainset.images)
