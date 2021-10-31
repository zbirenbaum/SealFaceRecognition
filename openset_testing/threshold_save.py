import os
import sys
import inspect
import facepy
import pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import pandas as pd
import numpy as np
import json
from pdb import set_trace as bp
from scipy import spatial
import operator
from meanfeatures import load_mean_features, save_mean_features, get_mean_features
#FALSE POSITIVE X AXIS
#TRUE POSITIVE Y AXIS

def threshcurve(evaldict):
    fpr = []
    tpr = []
    for t in np.arange(.3, 1, .02):
        tup = variable_thresh(evaldict, t)
        tpr.append(tup[0])
        fpr.append(tup[1])
    return np.array(fpr),np.array(tpr)
        

def variable_thresh(evaldict, threshold):
    predarray= []
    acceptlist = [] # probes that have similarity score >= THRESHOLD
    deniedlist = [] # probes that have similarity score < THRESHOLD
    positive = 0
    negative = 0
    
    for probelabel, probeinfo in evaldict.items():
        scores = probeinfo['scores']    
        inset = probeinfo['inset']    

        # Calculate the ranking of each prediction
        rank = 0
        if (inset):
            count = 1
            while (scores[count - 1][0] != probelabel): 
                count+=1
            rank = count
        else:
            rank = -1

        # remove redundant paths
        nameprobelabel = probelabel[probelabel.rfind('/')+1:]

        namescorelabel = scores[0][0] # rank-1 scores
        namescorelabel = namescorelabel[namescorelabel.rfind('/')+1:]
        predarray.append(namescorelabel)
        
        if scores[0][1] < threshold:
            deniedlist.append([nameprobelabel,
                namescorelabel, 
                scores[0][1],
                inset,
                rank])
        else:
            acceptlist.append([nameprobelabel,
                namescorelabel,
                scores[0][1],
                not inset,
                rank])
        
        if inset:
            positive +=1
        else:
            negative +=1
            

    pd.set_option('display.max_rows', 10000)

    full_list = deniedlist[:]
    full_list.extend(acceptlist)

    dnframe = pd.DataFrame(data=deniedlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score', 'False Reject', 'Rank'])
    accframe = pd.DataFrame(data=acceptlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score','False Accept', 'Rank'])
    fullframe = pd.DataFrame(data=full_list, columns=['Probe Label', 'Highest Score Label', 'Highest Score','False Accept', 'Rank'])
    tpr = (~accframe['False Accept']).values.sum()/positive #type: ignore
    fpr = accframe['False Accept'].values.sum()/negative #type: ignore
    return (tpr,fpr)
