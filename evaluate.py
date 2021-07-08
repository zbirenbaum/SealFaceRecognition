# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:17:56 2018

@author: Debayan Deb
"""
from __future__ import division
from network import Network
import sys
import utils
import facepy.evaluation as fev
import facepy
import numpy as np
import summary
import pandas as pd

def _find(l, a):
    return [i for (i, x) in enumerate(l) if x == a]


class ImageSet:

    def __init__(self, image_paths, config):
        self.image_paths = image_paths
        self.config = config
        self.images, self.labels = self.parse()
        self.features = None
    def parse(self):
        lines = [line.strip().split(' ') for line in self.image_paths]
        lines = lines[1:] #start at index 1
        return utils.preprocess([line[0] for line in lines], self.config, False), [line[1] for line in lines]

    def extract_features(self, model, batch_size):
        self.features = model.extract_feature(self.images, batch_size)

def identify(logdir, probe, gallery):

    uq = list(dict.fromkeys(gallery.labels))
    galFeaturesList = []
    for i in range(len(uq)):
        idx = _find(gallery.labels, uq[i])
        # Get feature vector for gallery images for the same indivdual
        galFeatures = gallery.features[idx]
        # individual feature vector from MAX, Mean, or Min template fusion
        individualFeatures = facepy.linalg.normalize(np.mean(galFeatures, axis=0))
        galFeaturesList.append(individualFeatures)

    score_matrix = facepy.metric.cosineSimilarity(probe.features, np.array(galFeaturesList))
    #score_matrix = facepy.metric.cosineSimilarity(probe.features, gallery.features)
#    print(score_matrix)
#   
    #print("Gallery Labels: " + str(gallery.labels))
    #print("Probe Labels: " + str(probe.labels))
    # Get ranks for each probe image
    with open(logdir + '/result.txt','w') as f:
        probelabelarr = []
        predlabelarr = []
        rank1matcharr = []
        rank5matcharr = []
        indexpredarr = []
        for i in range(len(probe.labels)):

            sort_idx = np.argsort(score_matrix[i])[::-1]
            predictions = np.array(uq)[sort_idx]
            rank = list(predictions).index(probe.labels[i]) + 1



            score = score_matrix[i][sort_idx][rank-1]

            prediction = predictions[0]


            probelabelarr.append(probe.labels[i])
            indexpredarr.append(rank-1)
            rank1matcharr.append(rank == 1)
            rank5matcharr.append(rank <= 5)
            predlabelarr.append(prediction)


#            print("Predictions:" + str(predictions))
#            print("Probe Label: " + str(probe.labels[i]))
#            print('Predicted Label: ' + predictions[0])

            f.write('{},{},{},{}\n'.format(probe.labels[i], rank, score, prediction))
        #resultdata = pd.Dataframe(columns=['ProbeLabel', 'PredictedLabel', 'Rank1Match', 'Rank5Match', 'IndexPredicted'))
        df = pd.DataFrame(
                data=list(zip(
                    probelabelarr, 
                    predlabelarr,
                    rank1matcharr, 
                    rank5matcharr, 
                    indexpredarr 
                    )),
                columns=[
                    'ProbeLabel', 
                    'PredictedLabel', 
                    'Rank1Match', 
                    'Rank5Match', 
                    'IndexPredicted'
                    ]
                )

        print(df)
        print('Totals:')
        print('Rank 1 Correct: ' + str(df.Rank1Match.sum()) + '/' + str(len(df.index))) 
        print('% Rank 1 Correct: {:.3f}'.format(df.Rank1Match.sum()/len(df.index)))
        print('Rank 5 Correct: ' + str(df.Rank5Match.sum()) + '/' + str(len(df.index)))
        print('% Rank 5 Correct: ' + str(df.Rank5Match.sum()/len(df.index)))
    return summary.run(logdir)


## Load Model
#network = Network()
#model_name = sys.argv[1]
#network.load_model(model_name)
#
#
#
#identify(probe_set, gal_set)    
#

