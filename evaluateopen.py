import facepy
import numpy as np
from scipy import spatial
import operator
import pandas as pd

def _find(l, a):
    return [i for (i, x) in enumerate(l) if x == a]
def get_threshold():
    #awful hardcode pls fix thx
    return 0.55

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
    acceptlist = []
    deniedlist = []
    
    score_vec = []
    label_vec = []

    threshold = get_threshold()
    for i in range(len(probe.labels)):
        evaldict[i] = {'probelabel': probe.labels[i], 
                'inset': probe.labels[i] in uq,
                'scores': {}
                }
        for j in range(len(uq)):
            evaldict[i]['scores'][uq[j]] = 1-spatial.distance.cosine(probe.features[i], galfeaturesdict[j]['features'])
            
        for gal, score in evaldict[i]['scores'].items():
            score_vec.append(score)
            if (probe.labels[i] == gal):
                label_vec.append(True)
            else:
                label_vec.append(False)
        
        
        predictions = sorted(evaldict[i]['scores'].items(), key=operator.itemgetter(1), reverse=True)
        
        predarray.append(predictions[0])
        if predictions[0][1] < threshold:
            deniedlist.append([probe.labels[i],
                predictions[0][0], 
                predictions[0][1],
                evaldict[i]['inset'] == True])
        else:
            acceptlist.append([probe.labels[i],
                predictions[0][0], 
                predictions[0][1],
                evaldict[i]['inset'] == False])
    
    facepy.plot.score_distribution(np.array(score_vec), np.array(label_vec))


    print(probe.labels[i] + " " + str(predictions[0]))
    dnframe = pd.DataFrame(data=deniedlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score', 'False Reject'])
    accframe = pd.DataFrame(data=acceptlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score','False Accept'])
    print(accframe)
    print('False Accepts: ' + str(accframe['False Accept'].sum()) + '/' + str(len(probe.labels)))
    print(dnframe)
    print('False Reject: ' + str(dnframe['False Reject'].sum()) + '/' + str(len(probe.labels)))
#        counter = 0
#        for prediction in predarray[i]:
#            print(prediction)
#            if counter == 5:
#                break
#            counter = counter +1
    return
def closed(probe, galFeaturesList):        
    score_matrix = facepy.metric.cosineSimilarity(probe.features, np.array(galFeaturesList))
    for i in range(len(probe.labels)):
        sort_idx = np.argsort(score_matrix[i])[::-1]
        predictions = np.array(uq)[sort_idx]
        print("{},{}\n".format(probe.image_paths[i], predictions[0]))


