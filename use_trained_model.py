import os
import tensorflow as tf
import traintestsplit as ttsplit
from network import Network
from argparse import ArgumentParser
import utils as ut
import evaluate


"""
First Need to generate closed set:
"""

def gen_kn_unknowns(testingdict):
    unique_labels_untrained = testingdict.keys()
    untrained_photos = ut.init_from_dict(testingdict)[3]
    return untrained_photos, unique_labels_untrained


def get_probes(testing_data, config):
    probes = ut.init_from_dict(testing_data)[3]
    probe_set = evaluate.ImageSet(probes, config)
    return probes, probe_set

def get_gal(training_data, config):
    gal = ut.init_from_dict(training_data)[3]
    gal_set = evaluate.ImageSet(gal, config)
    return gal, gal_set


def gen_sets(settings, config, num_trainings):
    builder = ttsplit.DatasetBuilder(settings.directory, usedict=1, settype='open', kfold=int(num_trainings))
    #for i in range(num_trainings):
    #    print('Starting evaluation #{}\n'.format(i+1))
    #galset = builder.dsetbyfold[i]
    testsetbyfold = builder.testsetbyfold
    probes = None
    probe_unique_labels = None
    gallery = []
    for i in range(num_trainings):
        if i == 0:
            probes = testsetbyfold[i]
            probe_unique_labels = probes.keys()
            continue
        else:
            for labelkey in testsetbyfold[i]:
                for path in testsetbyfold[i][labelkey]:
                    gallery.append(str(path) + ' ' + str(labelkey))
    print(gallery)
        





def get_features(probe_set, gal_set):
    """
    these functions set a variable in the dataclass class 
    so idk if necessary tbh
 
    """
    probe_features = probe_set.extract_features(network, len(probes))
    gal_features = gal_set.extract_features(network, len(gal))
    return probe_features, gal_features

def split_untrained_labels(untrained_labels):
    """
    This function splits labels unused in the training set
    Half of the labels go into the gallary as 'known unknowns'
    the other half are retained: e.g. label not in gallary

    Known Unknowns: Tests ability to predict labels not trained on
    Unknown Unknowns: Tests ability to detect faces not in gallary
    """
    kn_unk = []
    un_unk = []
    num_untrained = len(untrained_labels)/2

    


def run_identification(config, trained_labels, untrained_labels):
    network = Network()
    network.initialize(config, trainset.total_num_classes)
    network.restore_model(config.restore_model, config.restore_scopes)


def main():
    parser = ArgumentParser(description='Train SealNet', add_help=False)
    parser.add_argument('-c','--config_file', dest='config_file', action='store', 
        type=str, required=True, help='Path to training configuration file', )
    parser.add_argument('-d','--directory', dest='directory', action='store', 
        type=str, required=True, help='Path to photo directory', )
    settings = parser.parse_args()
    config = ut.import_file(settings.config_file, 'config')
    num_trainings = 5
    print('Running training {} times'.format(num_trainings))
    gen_sets(settings, config, num_trainings)


if __name__ == '__main__':
    main()
