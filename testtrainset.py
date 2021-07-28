import pandas as pd
import numpy as np
import utils
from network import Network
import traintestsplit as ttsplit
from pdb import set_trace as bp

config = utils.import_file('config.py', 'config')
num_trainings = 5
builder = ttsplit.DatasetBuilder(
        photodir='data/processed/',
        usedict=1,
        settype='both',
        kfold=int(num_trainings)
        )

#print(builder.dsetbyfold[0].set_list)
trainset = builder.dsetbyfold[0]
testset = builder.testsetbyfold[0]
probe_set = builder.probesetbyfold[0]
print(len(testset))
