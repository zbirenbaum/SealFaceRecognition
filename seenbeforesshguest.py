# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:17:56 2018
@author: Debayan Deb
"""
import os
from network import Network
import sys
import utils
import facepy.evaluation as fev
import facepy
import summary
from evaluateopen import identify
import traintestsplit as ttsplit



class ImageSet:
    def __init__(self, image_paths, config):
        self.image_paths = image_paths
        self.config = config
        self.images, self.labels = self.parse()
        self.features = None
    def parse(self):
        lines = [line.strip().split(' ') for line in self.image_paths]
        return utils.preprocess([line[0] for line in lines], self.config, False), [line[1] for line in lines]
    def extract_features(self, model, batch_size):
        self.features = model.extract_feature(self.images, batch_size)

def get_model_dirs(model_dir):
    modelslist = []
    for model in os.listdir(model_dir):
        modelslist.append(os.path.join(model_dir, model))
    if len(modelslist) == 0:
        exit(1)
    return modelslist


def main():

    model_dir = '/home/sshguest/research/SealFaceRecognition/testingmodel/'
    network = Network()
    config_file = 'config.py'
    config = utils.import_file(config_file, 'config')
   
    modelslist = get_model_dirs(model_dir)  
#    builder = ttsplit.DatasetBuilder(
#            photodir='data/fulldataset/2019data',
#            usedict=1,
#            settype='closed',
#            kfold=int(5)
#            )

#    closedsetprobes = builder.probesetbyfold[0]

#    gal = builder.dsetbyfold[0].set_list

#    opensetprobes = ttsplit.create_split_probe_dict(dir='data/openset/Mitchell_Field_Singles_1_31Chips',startat=len(closedsetprobes))

#    print(opensetprobes.keys())
#    opensetprobes.update(closedsetprobes)
#    probes = utils.init_from_dict(opensetprobes)[3]
    gal = []
    probes = []

    with open("./splits/both/fold1/probe.txt" ,'r') as f:
        counter = 0
        for line in f:
            if counter == 0:
                counter = 1
                continue
            probes.append(line.strip())

    probe_set = ImageSet(probes, config)
    #probe_set.extract_features(network, len(probes))
    #
    with open("./splits/both/fold1/train.txt", 'r') as f:
        counter = 0
        for line in f:
            if counter == 0:
                counter = 1
                continue
            gal.append(line.strip())
    gal_set = ImageSet(gal, config)
    #probe_set = ImageSet(probes, config)
    #gal_set = ImageSet(gal, config)

    model_name = modelslist[0]
    network.load_model(model_name)

    probe_set.extract_features(network, len(probes))
    gal_set.extract_features(network, len(gal))
    identify(probe_set, gal_set)
if __name__ == "__main__":
    num_models = 5 
     
    network = Network()
    main()
