# -*- coding: utf-8 -*-
import os
import sys
import inspect
import pandas as pd
import numpy as np

import argparse
import json
import matplotlib.pyplot as plt
import thresheval as t_eval
from load_mean_features import load_identify, load_mean_features

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import utils

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

def load_from_cache(model_name):
    evaldict = load_identify(model_name)
    return evaldict

def create_and_cache(model_name, fold):
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir) 
    from network import Network
    import meanfeatures as mf
    import utils

    network = Network()
    config_file = '../config.py'
    config = utils.import_file(config_file, 'config')
    network.load_model(model_name)
    gal = json_to_list('../openset_splits/' + str(fold) + '/'  + 'train.json')
    probes = json_to_list('../openset_splits/' + str(fold) + '/'  + 'validation.json')
    probes.extend(json_to_list('../openset_splits/' + str(fold) + '/'  + 'test.json'))

    gal_set = ImageSet(gal, config)
    probe_set = ImageSet(probes, config)

    gal_set.extract_features(network, len(gal))
    probe_set.extract_features(network, len(probes)//4)
    print(len(probe_set.features))
    evaldict = mf.identify(model_name, probe_set, gal_set, do_cache=True)
    return evaldict

def get_best(model, fold, do_cache):
    cache = model+"/cache"
    if not os.path.exists(cache):
        os.mkdir(cache)
    evaldict=None
    if do_cache:
        try:
            evaldict = load_from_cache(model)
            # evaldict = create_and_cache(model, fold)
        except:
            evaldict = create_and_cache(model, fold)
    else:
        evaldict = create_and_cache(model, fold)
    el = t_eval.EvalList(evaldict)
    return el

def main():
    # for model_dir in os.listdir('models_by_fold/'): #PrimNet or SealNet
    # models_folds = sorted(get_model_dirs('models_by_fold/'+model_dir))
    models = []
    for i in range(2,6):
        prefix = 'models_by_fold/SealNet/SealNet' + str(i) + "/"
        model=get_model_dirs(prefix)[0]
        el = get_best(model,1,do_cache=True)
        best = el.find_best()
        best.print()
    # models = sorted(models)
    # for model in models:
    #     get
    #     el = 
if __name__ == "__main__":
    main()
