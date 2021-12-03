import numpy as np
from calculations import Eval

class EvalList:
    def __init__(self,evaldict,increment=.01):
        self.evals = thresheval(evaldict,increment)
        self.best = self.find_best()
        
    def find_best(self):
        prev = 0
        best = None
        
        for eval in self.evals:
            if eval.f_measure > prev:
                prev = eval.f_measure
                best = eval
                print(eval.f_measure)
        return best

    def print_best(self):
        self.best.print() #type: ignore
        
    def get_best(self):
        return self.best

def thresheval(evaldict, increment):
    eval_array = []
    for t in np.arange(.0, 1, increment):
        eval_array.append(Eval(evaldict,t, 1))
    return eval_array


