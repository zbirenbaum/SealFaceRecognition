from matplotlib import test
import utils as ut
import traintestsplit as tt


#builder = tt.DatasetBuilder('photos', usedict=1, settype='closed', kfold=5)
#list_len = []
#for i in range(5):
#        print('Starting training #{}\n'.format(i+1))
#        trainset = builder.dsetbyfold[i]
#        testset = builder.testsetbyfold[i]
#        list_len.append([len(testset[key]) for key in testset.keys()])
#        probes = ut.init_from_dict(testset)[3]
#        print(len(probes))
#        print(list_len[i])
