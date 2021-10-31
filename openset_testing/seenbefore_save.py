# -*- coding: utf-8 -*-
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from network import Network
import utils
import threshold_save as evaluateopen
import threshold_save as vt
import meanfeatures as mf
import json
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import numpy as np
import calculations as calc

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

def display_graph(fpr,tpr):
    #print(fpr, tpr)
#    X_Y_Spline = make_interp_spline(fr, fa))
#    X_ = np.linspace(fr.min(), fr.max(), fa.max())
#    Y_ = X_Y_Spline(X_)
    plt.plot(fpr, tpr)
    plt.title("Plot Smooth Curve Using the scipy.interpolate.make_interp_spline() Class")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()

def json_to_list(filename):
    dct = None
    ls = []
    with open(filename, 'r') as f:
        dct = json.load(f)
        f.close()
    for key in dct:
        vals = dct[key]
        for val in vals:
            ls.append(val + " " + key)      
    return ls

def get_model_dirs(model_dir):
    modelslist = []
    for model in os.listdir(model_dir):
        modelslist.append(os.path.join(model_dir, model))
    if len(modelslist) == 0:
        exit(1)
    return modelslist


def main():

    model_dir = './models/'
    network = Network()
    config_file = '../config.py'
    config = utils.import_file(config_file, 'config')
    
    modelslist = get_model_dirs(model_dir)  
    model_name = modelslist[0]
#    model_name = model_dir + 'graph.meta'
    network.load_model(model_name)
    
    gal = json_to_list('../openset_splits/train.json')
    probes = json_to_list('../openset_splits/validation.json')
    # TODO Add in openset   
    probes.extend(json_to_list('../openset_splits/test.json'))

    gal_set = ImageSet(gal, config)
    probe_set = ImageSet(probes, config)
    
    probe_set.extract_features(network, len(probes))
    gal_set.extract_features(network, len(gal))
    
    #evaldict = mf.identify(probe_set, gal_set)
    evaldict = mf.load_identify()
    el = calc.EvalList(evaldict) 
    el.print_best()
    
    
    
    # out_file = open("result.json", "w")
    # json.dump(evaldict, out_file)
    # out_file.close()
    # fpr,tpr = vt.threshcurve(evaldict)
    # display_graph(fpr,tpr)
 #    evaluateopen.displayTestingResult(evaldict)
    

# 
#     with open("../openset_splits/validation.json" ,'r') as f:
#         for line in f:
#             probes.append(line.strip())
# 
#     probe_set = ImageSet(probes, config)
# 
#     with open("./referencePhotos.txt", 'r') as f:
#         for line in f:
#             gal.append(line.strip())
#     gal_set = ImageSet(gal, config)
# 
#     model_name = modelslist[0]
#     network.load_model(model_name)
# 
#     probe_set.extract_features(network, len(probes))
#     gal_set.extract_features(network, len(gal))
#     evaldict = evaluateopen.identify(probe_set, gal_set)
#     
#     # storing results into json format
#     out_file = open("result.json", "w")
#     json.dump(evaldict, out_file)
#     out_file.close()
#     
#     evaluateopen.displayTestingResult(evaldict)
    
    
if __name__ == "__main__":
    main()
