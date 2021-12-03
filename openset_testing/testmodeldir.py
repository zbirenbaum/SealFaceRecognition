# -*- coding: utf-8 -*-
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from network import Network
import utils
import argparse
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Model directory e.g. models/SealNet1")
   # parser.add_argument("-n", "--name", help="Model name e.g. sealnet")
    args=parser.parse_args()
    model_dir = args.dir
   # model_name = args.name
    network = Network()
    config_file = '../config.py'
    config = utils.import_file(config_file, 'config')
    
    modelslist = get_model_dirs(model_dir)  
    print(modelslist)
    model_name = modelslist[0]
    print("FUUUUUUCK\n")
#    model_name = model_dir + 'graph.meta'
main()
