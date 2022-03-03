import numpy as np
from calculations import Eval

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
    for eval in evals:
        if eval.fpr > .01:
            continue
        else:
            best = eval
            break
    return best

class EvalList:
    def __init__(self,evaldict, method="far", increment=.01):
        self.evals = thresheval(evaldict,increment)
        self.method = method
        self.best = self.find_best()
        
    def find_best(self):
        return eval(self.method)(self.evals)

    def print_best(self):
        self.best.print() #type: ignore
        
    def get_best(self):
        return self.best

def thresheval(evaldict, increment):
    eval_array = []
    for t in np.arange(.0, 1, increment):
        eval_array.append(Eval(evaldict,t, 1))
    return eval_array


