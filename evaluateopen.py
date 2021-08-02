import facepy
import numpy as np
from scipy import spatial
import operator
import pandas as pd

THRESHOLD = 0.6

def _find(l, a):
    return [i for (i, x) in enumerate(l) if x == a]

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


def identify(probe, gallery):
    uq = list(dict.fromkeys(gallery.labels))
    _, galfeaturesdict= get_mean_features(gallery, uq)
    
    evaldict = {}
    
    # evaldict = map probe labels to prediction
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
        
    return evaldict

def displayTestingResult(evaldict):
    predarray= []
    acceptlist = [] # probes that have similarity score >= THRESHOLD
    deniedlist = [] # probes that have similarity score < THRESHOLD
    
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
        print(probelabel)
        nameprobelabel = probelabel[probelabel.rindex('/')+1:]

        namescorelabel = scores[0][0] # rank-1 scores
        namescorelabel = namescorelabel[namescorelabel.rindex('/')+1:]
        predarray.append(namescorelabel)
        
        if scores[0][1] < THRESHOLD:
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

    pd.set_option('display.max_rows', 10000)

    full_list = deniedlist[:]
    full_list.extend(acceptlist)

    dnframe = pd.DataFrame(data=deniedlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score', 'False Reject', 'Rank'])
    accframe = pd.DataFrame(data=acceptlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score','False Accept', 'Rank'])
    fullframe = pd.DataFrame(data=full_list, columns=['Probe Label', 'Highest Score Label', 'Highest Score','False Accept', 'Rank'])
    
    print(accframe)
    print('False Accepts: ' + str(accframe['False Accept'].sum()) + '/' + str(len(evaldict)))
    print(dnframe)
    print('False Reject: ' + str(dnframe['False Reject'].sum()) + '/' + str(len(evaldict)))

    accuracyframe=fullframe.loc[fullframe['Rank'] != -1]
    accuracytotal = len(list(accuracyframe.index))
    correct1 = len(accuracyframe.loc[accuracyframe['Rank'] == 1])
    correct5 = len(accuracyframe.loc[accuracyframe['Rank'] <= 5])
    print('ACCURACY Rank 1: {:.3f}'.format(correct1/accuracytotal))
    print('ACCURACY Rank 5: {:.3f}'.format(correct5/accuracytotal))
    print('AVG Closed Score: ' + str(fullframe.loc[fullframe['Rank'] != -1]['Highest Score'].mean()))
    print('AVG Open Score: ' + str(fullframe.loc[fullframe['Rank'] == -1]['Highest Score'].mean()))

    print('AVG Accepted Score: ' + str(accframe['Highest Score'].mean()))
    print('AVG Denied Score: ' + str(dnframe['Highest Score'].mean()))
    print('AVG False Reject Score: ' + str(dnframe.loc[dnframe['Rank'] != -1]['Highest Score'].mean()))
    print('AVG True Reject Score: ' + str(dnframe.loc[dnframe['Rank']==-1]['Highest Score'].mean()))


def closed(probe, galFeaturesList):        
    score_matrix = facepy.metric.cosineSimilarity(probe.features, np.array(galFeaturesList))
    for i in range(len(probe.labels)):
        sort_idx = np.argsort(score_matrix[i])[::-1]
        predictions = np.array(uq)[sort_idx]
        print("{},{}\n".format(probe.image_paths[i], predictions[0]))


