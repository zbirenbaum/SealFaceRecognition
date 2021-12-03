import pickle
def load_identify(model_name):
    pickle_obj = open(model_name+"/cache/id.pickle", "rb")
    dict = pickle.load(pickle_obj)
    pickle_obj.close()
    return dict

def load_mean_features(model_name):
    pickle_obj = open(model_name+"/cache/features.pickle", "rb")
    dict = pickle.load(pickle_obj)
    pickle_obj.close()
    return dict
   # print(setFeaturesList)
