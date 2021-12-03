# -*- coding: utf-8 -*-
import os
import sys
import inspect
import pandas as pd

import argparse
import json
import matplotlib.pyplot as plt
import thresheval as t_eval
from load_mean_features import load_identify, load_mean_features

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


def load_from_cache(model_name):
        evaldict = load_identify(model_name)
        return evaldict

def create_and_cache(model_name):
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
    
    print("No cached pickle, creating one")

    gal = json_to_list('../openset_splits/train.json')
    probes = json_to_list('../openset_splits/validation.json')
# TODO Add in openset   
    probes.extend(json_to_list('../openset_splits/test.json'))

    gal_set = ImageSet(gal, config)
    probe_set = ImageSet(probes, config)

    probe_set.extract_features(network, len(probes))
    gal_set.extract_features(network, len(gal))
    evaldict = mf.identify(model_name,probe_set, gal_set)
    return evaldict
    
def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-d", "--dir", help="Model directory e.g. models/SealNet1")
   # parser.add_argument("-n", "--name", help="Model name e.g. sealnet")
    #args=parser.parse_args()
    #model_dir = args.dir
   # model_name = args.name
#    model_name = model_dir + 'graph.meta'
    

    result_dict = {}
    for model_dir in os.listdir('models/'):
        modelslist = get_model_dirs('models/'+model_dir)  
        #print(modelslist)
        model_name = modelslist[0]
        
        cache = model_dir+"/"+model_name+"/"+"cache"
        evaldict=None
        
        try:
            evaldict = load_from_cache(model_name)
        except:
            evaldict = create_and_cache(model_name)
            
        el = t_eval.EvalList(evaldict) 
        best = el.get_best()
        print(model_name + ': ' + str(best.threshold)) #type: ignore
        result_dict[model_dir] = best.to_df() #type: ignore
    result_dict['Difference']=result_dict['SealNet']-result_dict['PrimNet']
    comparison_df = pd.concat(result_dict.values(), axis=0, keys=result_dict.keys())
    comparison_df = comparison_df.reindex(['SealNet', 'PrimNet', 'Difference'], level=0)
    #comparison_df["Difference"] = comparison_df.SealNet.sub(comparison_df.PrimNet)
    print(comparison_df)
    print("Writing df to comparison.xlsx")
    comparison_df.to_excel("comparison.xlsx")
    print("Written")
    
    
    
    
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
