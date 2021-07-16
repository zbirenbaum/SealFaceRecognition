import facepy
import numpy as np
from scipy import spatial
import operator

def _find(l, a):
    return [i for (i, x) in enumerate(l) if x == a]

def identify(probe, gallery):
    galfeaturesdict = {} 
    uq = list(dict.fromkeys(gallery.labels))
    galFeaturesList = []
    for i in range(len(uq)):
        idx = _find(gallery.labels, uq[i])
        # Get feature vector for gallery images for the same indivdual
        galFeatures = gallery.features[idx]
        # individual feature vector from MAX, Mean, or Min template fusion
        individualFeatures = facepy.linalg.normalize(np.mean(galFeatures, axis=0))
        galFeaturesList.append(individualFeatures)
        galfeaturesdict[i] = {'idx': idx, 'label': uq[i], 'features': individualFeatures}

    evaldict = {}
    predarray= []
    for i in range(len(probe.labels)):
        evaldict[i] = {'probelabel': probe.labels[i], 
                'inset': probe.labels[i] in uq,
                'scores': {}
                }
        for j in range(len(uq)):
            evaldict[i]['scores'][uq[j]] = 1-spatial.distance.cosine(probe.features[i], galfeaturesdict[j]['features'])
        predictions = sorted(evaldict[i]['scores'].items(), key=operator.itemgetter(1), reverse=True)
        predarray.append(predictions)
        print('Probelabel' + str(i) + 'Similarity Scores')
        print('TOP 5 RANKED') 
        counter = 0
        for prediction in predarray[i]:
            print(prediction)
            if counter == 5:
                break
            counter = counter +1
    return
def closed(probe, galFeaturesList):        
    score_matrix = facepy.metric.cosineSimilarity(probe.features, np.array(galFeaturesList))
    for i in range(len(probe.labels)):
        sort_idx = np.argsort(score_matrix[i])[::-1]
        predictions = np.array(uq)[sort_idx]
        print("{},{}\n".format(probe.image_paths[i], predictions[0]))


