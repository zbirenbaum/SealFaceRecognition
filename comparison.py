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
        print(lines)
        #return [line[0] for line in lines], [line[1] for line in lines]
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


def load_split(foldnum, filename):
    with open("splitsave/" + str(foldnum+1) + "/" + filename + ".json", "r") as infile:
        return json.load(infile)
    
def main():

    #model_dir = './trainedModel/20211015-101706/graph.meta'
    
    model = './models_for_comparison/sealnet/SealNet_Fold3/20211015-100334/'
    network = Network()
    network.load_model(model)
    config_file = 'config.py'
    config = utils.import_file(config_file, 'config')
   
    #modelslist = get_model_dirs(model_dir)  
#    modelslist = ['./trainedModel/sealnet/SealNet_Fold1/20211015-094735/']
    gal = []
    probes = []

            
    testdata = load_split(2, 'test')
    for k in testdata.keys():
        for path in testdata[k]:
            newstr = path  + ' ' + path[:path.rfind('/')] 
            print(newstr)
            probes.append(newstr)
    print(probes)
            
    probe_set = ImageSet(probes, config)
    
    galdata = load_split(2, 'test')
    for k in galdata.keys():
        for path in galdata[k]:
            probes.append(path  + ' ' + path[:path.rfind('/')])

    gal_set = ImageSet(gal, config)

    #model_name = modelslist[0]
    network.load_model(model)

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
