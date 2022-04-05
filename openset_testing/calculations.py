import pandas as pd
# Accuracy: Overall, how often is the classifier correct?
#     (TP+TN)/total = (100+50)/165 = 0.91



class Eval:
    def __init__(self, evaldict, threshold, rank):
        self.rank = rank
        self.threshold = threshold
        self.base_metrics = get_base_metrics(evaldict,threshold, rank)
        self.set_metrics()
        if rank == 1:
            self.r5 = Eval(evaldict, threshold, 5)
        self.calc_metrics()
        self.metrics = self.to_dict()

    def set_metrics(self):
        self.tp = self.base_metrics[0]
        self.tn = self.base_metrics[1]
        self.fp = self.base_metrics[2]
        self.fn = self.base_metrics[3]

    def calc_metrics(self):
        self.tpr = self.calc_sensitivity() #sensitivity/recall
        self.fpr = self.calc_false_positive_rate()
        self.fnr = self.calc_false_negative_rate()
        self.tnr = self.calc_specificity()
        self.baseline_accuracy = self.calc_baseline_accuracy()
        self.accuracy = self.calc_accuracy()
        self.precision = self.calc_precision()
        self.f_measure = self.calc_f_measure()


    def get_dict(self):
        as_dict = {
                "TPR": self.tpr, 
                "FPR": self.fpr, 
                "FNR": self.fnr, 
                "TNR": self.tnr,
                "Baseline Accuracy": self.baseline_accuracy,
                "Accuracy": self.accuracy, 
                "Precision": self.precision,
                "F-Measure": self.f_measure,
                "Threshold": self.threshold
                }
        return as_dict

    def to_dict(self):
        return self.get_dict()

    def calc_false_positive_rate(self):
        self.fpr = self.fp/(self.fp+self.tn)
        return self.fpr

    def calc_false_negative_rate(self):
        self.fnr = 1-self.tpr
        return self.fnr

    def calc_specificity(self):
        #True Negative Rate
        specificity = self.tn/(self.tn+self.fp)
        return specificity

    def calc_baseline_accuracy(self):
        acc = (self.tn)/(self.tp + self.tn + self.fp + self.fn)
        return acc

    def calc_accuracy(self):
        acc = (self.tp + self.tn)/(self.tp + self.tn + self.fp + self.fn)
        return acc

    def calc_precision(self): 
        if self.tp == 0:
            return 0
        precision = self.tp/(self.tp + self.fp)
        return precision

    def calc_sensitivity(self):
        #true positive rate (self.tpr)
        #also known as recall
        if self.tp == 0:
            return 0
        sensitivity = self.tp/(self.tp+self.fn)
        #if this errors, threshold is too high
        return sensitivity

    def calc_f_measure(self):
        if self.tp == 0:
            return 0
        f_measure = (2*self.tpr * self.precision)/(self.tpr + self.precision)
        return f_measure

    def to_df(self):
        return pd.DataFrame(data=[self.to_dict(), self.r5.to_dict()], index=['R1', 'R5'])

    def print(self):
        print("THRESHOLD: " + str(self.threshold))
        print("R1 Metrics:")
        print("True Positive: "  + str(self.tp))
        print("False Positive: " + str(self.fp))
        print("True Negative: "  + str(self.tn))
        print("False Negative: " + str(self.fn))
        print("Accuracy: " + str(self.accuracy))
        print("Precision:" + str(self.precision))
        print("F1-Score: " + str(self.f_measure))
        print("\nR5 Metrics:")
        print("True Positive: "  + str(self.r5.tp))
        print("False Positive: " + str(self.r5.fp))
        print("True Negative: "  + str(self.r5.tn))
        print("False Negative: " + str(self.r5.fn))
        print("Accuracy: " + str(self.r5.accuracy))
        print("Precision:" + str(self.r5.precision))
        print("F1-Score: " + str(self.r5.f_measure))
        print("\n")


def get_base_metrics(evaldict, threshold, rank_cutoff):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for probelabel, probeinfo in evaldict.items():
        probelabel = probelabel[0:probelabel.index('+')]
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
