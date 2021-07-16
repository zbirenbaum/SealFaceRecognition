
import sys
import os
#import warnings

from tensorflow.python.ops.variables import initialize_all_variables

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
#sys.stderr = open(os.devnull, "w")  # silence stderr
#warnings.filterwarnings('ignore')
import tensorflow as tf
from argparse import ArgumentParser
import utils
from network import Network
import evaluate
import traintestsplit as ttsplit
import math
import nets.seal_net_old as seal_net


def get_model_checkpoints(config):
    modelslist = []
    for model in os.listdir(config.restore_model):
        modelslist.append(os.path.join(config.restore_model, model))
    if len(modelslist) == 0:
        print('NO MODELS IN RESTORE DIR')
        exit(1)
    return modelslist

def get_data(builder, counter):
    gallery = builder.dsetbyfold[counter]
    probes = builder.probesetbyfold[counter]
    return gallery, probes

def override_batch_size(gallery, divisor):
    batch_size = math.ceil(len(gallery)/divisor)
    epoch_size = divisor
    return batch_size, epoch_size

def test_model(gal, probes, config, counter, model, network):
    config.batch_size, config.epoch_size = override_batch_size(gal.set_list, 3)
    ckpt = tf.train.get_checkpoint_state(model)
   
    gal = gal.set_list# delete later, gallary set equal to training prior to preprocess
    
    probes = utils.init_from_dict(probes)[3]
    probe_set = evaluate.ImageSet(probes, config)

    gal_set = evaluate.ImageSet(gal, config)
    # Initalization log and summary for running
    log_dir = utils.create_log_dir(config, config_file, 'SealNet_Fold{}'.format(counter))
    
    print('Testing...')
    probe_set.extract_features(network, len(probes))
    gal_set.extract_features(network, len(gal))

    rank1, rank5, df = evaluate.identify(log_dir, probe_set, gal_set)
    print(df)
    print('rank-1: {:.3f}, rank-5: {:.3f}'.format(rank1[0], rank5[0]))
    
    # Output test result


def main(settings, config, num_models):
    print('Running testing {} times'.format(num_models))
    modelslist = []
    modelslist = get_model_checkpoints(config)
    for i in range(num_models):
        gal, probes = get_data(builder, i)
        print('Starting training #{}\n'.format(i+1))
        #gallery = builder.dsetbyfold[i]
        #testset = builder.testsetbyfold[i]
        #probeset = builder.probesetbyfold[i]
        print('wat') 
        test_model(gal, probes, config, i+1, modelslist[i])
if __name__ == '__main__':
    parser = ArgumentParser(description='Train SealNet', add_help=False)
    parser.add_argument('-c','--config_file', dest='config_file', action='store', 
        type=str, required=True, help='Path to training configuration file', )
    parser.add_argument('-d', '--directory', dest='directory', action='store',
        type=str, required=True, help='Directory containing subdirectories that contain photos')
    parser.add_argument('-s', '--splits', dest='splits', action='store', type=bool,
        required=False, help='Flag to use existing splits for training and testing data')
    parser.add_argument('-n', '--number', dest='number', action='store', type=int,
        required=False, help='Number of times to run the training(default is 5)')
    settings = parser.parse_args()
     
    config_file = 'config.py' if not settings.config_file else settings.config_file
    config = utils.import_file(config_file, 'config')

    num_models = 5 
    if settings.number:
        num_models = settings.number
    
    network = Network()
    modelslist = get_model_checkpoints(config)  
    builder = ttsplit.DatasetBuilder(
            settings.directory,
            usedict=1,
            settype=config.testing_type,
            kfold=int(num_models)
            )
   # for fold in range(num_trained):
   #     saver = tf.train.Saver()
   #     network.restore_model(sess,modelslist[fold])
    main(settings, config, num_models)

