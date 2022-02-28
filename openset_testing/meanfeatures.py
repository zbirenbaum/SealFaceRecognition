import os
import sys
import inspect
import facepy
import pickle

from openset_testing.load_mean_features import load_identify
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import pandas as pd
import numpy as np
import json
#from pdb import set_trace as bp
from scipy import spatial
import operator
from load_mean_features import load_mean_features load_identify


def _find(l, a):
    return [i for (i, x) in enumerate(l) if x == a]

def save_mean_features(model_name, set, label_list):
    setfeaturesdict = {} 
    uq = label_list 
    setFeaturesList = []
    for i in range(len(uq)):
        idx = _find(set.labels, uq[i])
        # Get feature vector for set images for the same indivdual
        setFeatures = set.features[idx]
        # individual feature vector from MAX, Mean, or Min template fusion
        individualFeatures = facepy.linalg.normalize(np.mean(setFeatures, axis=0))
        setFeaturesList.append(individualFeatures)
        setfeaturesdict[i] = {'idx': idx, 'label': uq[i], 'features': individualFeatures}
#    with open("test.txt", "w") as f:
    #json.dump("test.txt",setfeaturesdict)
    pickle_obj = open(model_name+"/cache/features.pickle","wb")
    pickle.dump(setfeaturesdict, pickle_obj)
    pickle_obj.close()
    return setfeaturesdict
#f.close()
    #return setFeaturesList, setfeaturesdict

def get_mean_features(set, label_list):
    setfeaturesdict = {} 
    uq = label_list 
    setFeaturesList = []
    for i in range(len(uq)):
        idx = _find(set.labels, uq[i])
        # Get feature vector for set images for the same indivdual
        setFeatures = set.features[idx]
        # individual feature vector from MAX, Mean, or Min template fusion
        individualFeatures = facepy.linalg.normalize(np.mean(setFeatures, axis=0))
        setFeaturesList.append(individualFeatures)
        setfeaturesdict[i] = {'idx': idx, 'label': uq[i], 'features': individualFeatures}

    return setFeaturesList, setfeaturesdict

def save_identify(model_name, evaldict):
    pickle_obj = open(model_name+"/cache/id.pickle","wb")
    pickle.dump(evaldict, pickle_obj)
    pickle_obj.close()

def identify(model_name, probe, gallery):
    uq = list(dict.fromkeys(gallery.labels))
    try:
        galfeaturesdict = load_mean_features(model_name)
    except:
        print("no feature dict found, creating one")
        galfeaturesdict = save_mean_features(model_name, gallery, uq)

    evaldict = {}
    for i in range(len(probe.labels)):
        probelabel = probe.labels[i]
        evaldict[probelabel] = { 
                'inset': probelabel in uq, # whether this probe label is in the set (for testing purposes)
                # In actual open-set, this is false by default because we do not know the actual identity of the probes
                'scores': [] # sorted predictions with each of the class in gallery, scores[i] = [ith_gallery_class, corresponding_similarity_score]
                }
        prediction = {}
        for j in range(len(uq)):
            prediction[uq[j]] = 1-spatial.distance.cosine(probe.features[i], galfeaturesdict[j]['features'])

        evaldict[probelabel]['scores'] = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    save_identify(model_name, evaldict)
    return evaldict


