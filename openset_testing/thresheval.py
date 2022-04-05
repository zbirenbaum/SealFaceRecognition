import numpy as np
from calculations import Eval
from multiprocessing import Pool

def fscore(evals):
    prev = 0
    best = None
    for eval in evals:
        if eval.f_measure > prev:
            prev = eval.f_measure
            best = eval
            print(eval.fpr)
    return best

def far(evals):
    best = None
    prev = 0
    closest = 1
    for eval in evals:
        dist = abs(eval.fpr - .01)
        if dist < closest and eval.fpr <= .01:
            best = eval
            closest=dist
        else:
            continue
    return best

class EvalList:
    def __init__(self,evaldict, method="far", increment=(1/(24*1000))):
    # def __init__(self,evaldict, method="far", increment=(1/(24*1))):
        self.evals = thresheval(evaldict,increment)
        self.method = method
        self.best = self.find_best()

    def find_best(self):
        return eval(self.method)(self.evals)

    def print_best(self):
        self.best.print() #type: ignore

    def get_best(self):
        return self.best

def mproc_eval(arg_tuple):
    # print(arg_tuple_list)
    return Eval(arg_tuple[0], arg_tuple[1], arg_tuple[2])

def pooltest(n):
    print(n)
    return n*n

def get_arange(tup):
    start, end, increment = (tup[0], tup[1], tup[2])
    return np.arange(start, end, increment)

def thresheval(evaldict, increment):
    # eval_array = []
    counter = 0
    joblist = [[]*24]
    inclist = []
    test_vals = []
    for i in range(25):
        inclist.append((i/25, (i+1)/25, increment))
    for t in np.arange(0, 1, increment):
        test_vals.append(t)

    # with Pool(processes=None) as pool:
    #     test_vals = pool.map(get_arange, (inclist))
    # print(test_vals)
    # joblist = [(evaldict, ent, 1) for sublist in test_vals for ent in sublist]
    # joblist = [ent for ent in test_vals]
    jobs = [(evaldict, t, 1) for t in test_vals]
    print(len(jobs))
    # for jobs in joblist:
    #     print(len(jobs))
    pool = Pool(None)
    evals_list = pool.map(mproc_eval,jobs, chunksize=(len(jobs)//10))
    pool.close()
    pool.join()
    return evals_list
    #     print(pool.map(pooltest, ))
    # for t in np.arange(.0, 1, increment):
    #     joblist[counter].append((evaldict, t, 1)) # split into 24 groups with args for each call
    # #     # joblist.append(t)
    # # print(len(joblist[23]))
    # with Pool() as p:
    #     print(evals)
    # #
    # return evals


