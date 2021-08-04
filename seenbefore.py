# -*- coding: utf-8 -*-
import os
from network import Network
import sys
import utils
import evaluateopen
import json

class ImageSet:
    def __init__(self, image_paths, config, probe=False):
        self.image_paths = image_paths
        self.config = config
        self.images, self.labels = self.parse()
        self.features = None
    def parse(self):
        lines = [line.strip().split(' ') for line in self.image_paths]
        return utils.preprocess([line[0] for line in lines], self.config, False), [line[1] for line in lines]
    def extract_features(self, model, batch_size):
        self.features = model.extract_feature(self.images, batch_size)
    def extract_features_mean(self, model, batch_size):
        samearr=[]
        for i in range(1, len(self.images)):
            prev = self.images[i-1]
            curr = self.images[i]
            if curr == prev:
                samearr.append()
        self.features = model.extract_feature(self.images, batch_size)

def get_model_dirs(model_dir):
    modelslist = []
    for model in os.listdir(model_dir):
        modelslist.append(os.path.join(model_dir, model))
    if len(modelslist) == 0:
        exit(1)
    return modelslist


def main():

    model_dir = './modeltesting/store/'
    network = Network()
    config_file = 'config.py'
    config = utils.import_file(config_file, 'config')
   
    modelslist = get_model_dirs(model_dir)  
    gal = []
    probes = []

    with open("./splits/both/fold1/probe.txt" ,'r') as f:
        for line in f:
            probes.append(line.strip())

    probe_set = ImageSet(probes, config)

    with open("./splits/both/fold1/train.txt", 'r') as f:
        for line in f:
            gal.append(line.strip())
    gal_set = ImageSet(gal, config)

    model_name = modelslist[0]
    network.load_model(model_name)

    probe_set.extract_features(network, len(probes))
    gal_set.extract_features(network, len(gal))
    evaldict = evaluateopen.identify(probe_set, gal_set)
    
    # storing results into json format
    out_file = open("result.json", "w")
    json.dump(evaldict, out_file)
    out_file.close()
    
    evaluateopen.displayTestingResult(evaldict)
    
    
if __name__ == "__main__":
    main()
