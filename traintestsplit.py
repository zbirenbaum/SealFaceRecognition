from pprint import pprint
import pprintpp as pp
import dirhandler2 as dh
import calcindices as ci
import numpy as np
import os
class Dataset(object):
    def __init__(self, photodir, kfold, exclude=None):
        self.photodir = photodir
        self.kfold = kfold
        if exclude is None:
            exclude = kfold
        self.exclude = exclude
        self.data = dh.gen_dict(photodir, self.exclude)
        self.open_ttdict = self.gen_open_ttdict()
        self.closed_ttdict = self.gen_closed_ttdict()
        self.write_ttdict('open')
        self.write_ttdict('closed')
        return

    def gen_closed_ttdict(self):
        closeddict = {}
        for fold in range (1, self.kfold+1):
            closeddict[fold] = {
                    'training':{},
                    'testing':{}
                    }
        for label in self.data.keys():
            labeldict = self.data[label]
            photolist = np.array(labeldict['photos'])
            photoidx_training, photoidx_testing = ci.calcindices([],[],0,len(photolist), self.kfold)
            for fold in range(1, self.kfold+1):
                photos_training = list(photolist[photoidx_training[fold-1]])
                photos_testing = list(photolist[photoidx_testing[fold-1]])
                closeddict[fold]['training'][label] = photos_training
                closeddict[fold]['testing'][label] = photos_testing
                        
        return closeddict

    def gen_open_ttdict(self):
        self.open_training_idx, self.open_testing_idx = ci.calcindices([],[],0,len(self.data.keys()), self.kfold)
        ttdict = {}
        for fold in range(1,self.kfold+1):
            ttdict[fold] = {
                    'training': {key : self.data[key]['photos'] for key in self.open_training_idx[fold-1]},
                    'testing': {key : self.data[key]['photos'] for key in self.open_testing_idx[fold-1]}
                    }
        return ttdict

    def write_ttdict(self, settype):
        for fold in range(1, self.kfold+1):
            if settype == 'closed':
                to_write_training = self.closed_ttdict[fold]['training']
                to_write_testing = self.closed_ttdict[fold]['testing']
                num_training_classes = len(to_write_training.keys())
                num_testing_classes = len(to_write_testing.keys())
            elif settype == 'open':
                to_write_training = self.open_ttdict[fold]['training']
                to_write_testing = self.open_ttdict[fold]['testing']
                num_training_classes = len(to_write_training.keys())
                num_testing_classes = len(to_write_testing.keys())
            else:
                return "ERROR"

            self.create_set(to_write_training, settype, 'train', fold, num_training_classes)
            self.create_set(to_write_testing, settype, 'test', fold, num_testing_classes)
        return

    
    def create_set(self, ttdict, settype, typett, fold, num_classes): 
        splits_dir = os.path.join(os.path.expanduser('./splits/{}/fold{}'.format(settype,fold)))
        if not os.path.isdir(splits_dir):
            os.makedirs(splits_dir)
        fname = './splits/{}/fold{}/{}.txt'.format(settype, fold, typett)
        with open(fname, 'w') as f:
            f.write('Total_Number_Of_Classes' + ' ' + str(num_classes) + '\n')
            for label in ttdict.keys():
                for photopath in ttdict[label]:
                    f.write(photopath + ' ' + str(label) + '\n')
        f.close()
        return
 
        #print(fold) 
 #       print('Training:')
 #       print(fold[0])
 #       print('Testing:')
 #       print(fold[1])

dset = Dataset('photos', 5)
#print_fold_idx(dset.open_fold_idx)
#print(dset.open_fold_idx)
