import facepy
import numpy as np
from scipy import spatial
import operator
import pandas as pd

def _find(l, a):
    return [i for (i, x) in enumerate(l) if x == a]
def get_threshold():
    #awful hardcode pls fix thx
    return 0.6


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
    galFeaturesList, galfeaturesdict= get_mean_features(gallery, uq)
    probe_labels_uq = list(dict.fromkeys(probe.labels))
#    probe.images, throwaway = get_mean_features(probe, probe_labels_uq)
#    probe.labels=probe_labels_uq
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
        nameprobelabel = probe.labels[i] 
        nameprobelabel = nameprobelabel[nameprobelabel.rindex('/')+1:]

        namescorelabel = predictions[0][0]
        namescorelabel = namescorelabel[namescorelabel.rindex('/')+1:]
        if predictions[0][1] < threshold:
            deniedlist.append([nameprobelabel,
                namescorelabel, 
                predictions[0][1],
                evaldict[i]['inset'] == True,
                evaldict[i]['inset']])
        else:
            acceptlist.append([nameprobelabel,
                namescorelabel,
                predictions[0][1],
                evaldict[i]['inset'] == False,
                evaldict[i]['inset']])
    
#    facepy.plot.score_distribution(np.array(score_vec), np.array(label_vec))

    pd.set_option('display.max_columns', 10000)
    pd.set_option('display.max_rows', 10000)

    print(probe.labels[i] + " " + str(predictions[0]))
    full_list = deniedlist[:]
    full_list.extend(acceptlist)

    dnframe = pd.DataFrame(data=deniedlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score', 'False Reject', 'In Set'])
    accframe = pd.DataFrame(data=acceptlist, columns=['Probe Label', 'Highest Score Label', 'Highest Score','False Accept', 'In Set'])
    fullframe = pd.DataFrame(data=full_list, columns=['Probe Label', 'Highest Score Label', 'Highest Score','False Accept', 'In Set'])
    
#    print(accframe)
    print('False Accepts: ' + str(accframe['False Accept'].sum()) + '/' + str(len(probe.labels)))
#    print(dnframe)
    print('False Reject: ' + str(dnframe['False Reject'].sum()) + '/' + str(len(probe.labels)))

#    print(fullframe.loc[fullframe['In Set']]['Highest Score'].mean())
#    print(fullframe.loc[fullframe['In Set']==False]['Highest Score'].mean())

    accuracyframe=fullframe.loc[accframe['In Set']]
    accuracytotal = len(list(accframe.index))
    correct = len(accframe.loc[accframe['Probe Label'] == accframe['Highest Score Label']].index)
    print(correct/accuracytotal)
    print('ACCURACY Rank 1: ' + str(len(fullframe.loc[fullframe['Probe Label'] == fullframe['Highest Score Label']].index)/len(fullframe.index)))
    print('AVG Closed Score: ' + str(fullframe.loc[fullframe['In Set']]['Highest Score'].mean()))
    print('AVG Open Score: ' + str(fullframe.loc[fullframe['In Set']==False]['Highest Score'].mean()))

    
    print('AVG Accepted Score: ' + str(accframe['Highest Score'].mean()))
    print('AVG Denied Score: ' + str(dnframe['Highest Score'].mean()))
    print('AVG False Reject Score: ' + str(dnframe.loc[dnframe['In Set']]['Highest Score'].mean()))
    print('AVG True Reject Score: ' + str(dnframe.loc[dnframe['In Set']==False]['Highest Score'].mean()))
    #fullframe.set_index(['Probe Label', 'Highest Score Label'], inplace=True)
    #print(fullframe)
    #print(fullframe.groupby('Probe Label').mean())

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


