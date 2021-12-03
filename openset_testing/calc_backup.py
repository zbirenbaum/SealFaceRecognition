from pdb import set_trace as bp
import numpy as np
# Accuracy: Overall, how often is the classifier correct?
#     (TP+TN)/total = (100+50)/165 = 0.91

class EvalList:
    def __init__(self,evaldict):
        self.evals = thresheval(evaldict)
        self.best = self.get_best()
        
    def get_best(self):
        prev = 0
        best = None
        
        for eval in self.evals:
            if eval.r1_acc > prev:
                prev = eval.r1_acc
                best = eval
        return best

    def print_best(self):
        self.best.print() #type: ignore
            
class Eval:
    def __init__(self, evaldict, threshold):
        self.threshold = threshold
        self.r1 = get_metrics(evaldict,threshold, 1)
        self.r5 = get_metrics(evaldict,threshold, 5)
        self.set_r1_metrics()
        self.set_r5_metrics()
        self.r1_acc = calc_accuracy(self.r1)
        self.r5_acc = calc_accuracy(self.r5)
        
    def set_r1_metrics(self):
        self.r1tp = self.r1[0]
        self.r1tn = self.r1[1]
        self.r1fp = self.r1[2]
        self.r1fn = self.r1[3]
        
    def set_r5_metrics(self):
        self.r5tp = self.r5[0]
        self.r5tn = self.r5[1]
        self.r5fp = self.r5[2]
        self.r5fn = self.r5[3]
        
    def print(self):
        print("THRESHOLD: " + str(self.threshold))
        print("R1 Metrics:")
        print("True Positive: "  + str(self.r1tp))
        print("False Positive: " + str(self.r1fp))
        print("True Negative: "  + str(self.r1tn))
        print("False Negative: " + str(self.r1fn))
        print("Accuracy: " + str(self.r1_acc))
        print("\nR5 Metrics:")
        print("True Positive: "  + str(self.r5tp))
        print("False Positive: " + str(self.r5fp))
        print("True Negative: "  + str(self.r5tn))
        print("False Negative: " + str(self.r5fn))
        print("Accuracy: " + str(self.r5_acc))
        print("\n")
        
def thresheval(evaldict):
    eval_array = []
    for t in np.arange(.0, 1, .02):
        eval_array.append(Eval(evaldict,t))
    return eval_array
#        tup = variable_thresh(evaldict, t)
#        tpr.append(tup[0])
#        fpr.append(tup[1])
#    return np.array(fpr),np.array(tpr)

def get_rank(scores, probelabel, inset):
    rank = 0
    if (inset):
        count = 1
        while (scores[count - 1][0] != probelabel): 
            count+=1
        rank = count
    else:
        rank = -1
    return rank

def get_metrics(evaldict, threshold, rank_cutoff):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for probelabel, probeinfo in evaldict.items():
        inset = probeinfo['inset']    
        scores = probeinfo['scores']    
        highscore = float(scores[0][1])
            
        if not inset:
            if highscore < threshold:
                tn += 1
            if highscore >= threshold:
                fp += 1
        elif inset:
            rank = get_rank(scores, probelabel, inset)
            if highscore >= threshold and rank <= rank_cutoff and rank > 0:
                tp += 1
            else:
                fn += 1
    return [tp,tn,fp,fn]

def calc_sensitivity(metric_arr):
    #true positive rate (tpr)
    #also known as recall
    tp = metric_arr[0]
    fn = metric_arr[3]
    sensitivity = tp/(tp+fn)
    return sensitivity

def calc_false_positive_rate(metric_arr):
    tn = metric_arr[1]
    fp = metric_arr[2]
    fpr = fp/(fp+tn)
    return fpr
    
def calc_false_negative_rate(metric_arr):
    tn = metric_arr[1]
    fn = metric_arr[3]
    fnr = fn/(fn+tn)
    return fnr

def calc_specificity(metric_arr):
    #True Negative Rate
    tn = metric_arr[1]
    fp = metric_arr[2]
    sensitivity = tn/(tn+fp)
    return sensitivity

def calc_baseline_accuracy(metric_arr):
    tp = metric_arr[0]
    tn = metric_arr[1]
    fp = metric_arr[2]
    fn = metric_arr[3]
    acc = (tn)/(tp + tn + fp + fn)
    return acc

def calc_accuracy(metric_arr):
    tp = metric_arr[0]
    tn = metric_arr[1]
    fp = metric_arr[2]
    fn = metric_arr[3]
    acc = (tp + tn)/(tp + tn + fp + fn)
    return acc

def eval_model(evaldict,threshold):
    #[tp,tn,fp,fn]
    r1 = get_metrics(evaldict,threshold, 1)
    r5 = get_metrics(evaldict,threshold, 5) 
    return r1,r5
#    r1_acc = calc_accuracy(r1)
#    r5_acc = calc_accuracy(r5) 

    
#if inset && > threshold true positive
#if 
    # Total TP = (7+2+1) = 10
    # Total FP = (8+9)+(1+3)+(3+2) = 26
    # Total FN = (1+3)+(8+2)+(9+3) = 26
