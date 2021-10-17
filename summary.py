import matplotlib.pyplot as plt
import numpy as np

def run(logdir, df):
    num_groups = 1
    num_inner = 1
    
    rank1 = []
    rank5 = []
    
    ha = 0
    hb = 0
    ma = 0
    mb = 0
    hc = 0
    mc = 0
    
    ranksets = []
    ta = 0
    fa = 0
    tr = 0
    fr = 0
    
    accScores = []
    rejScores = []
    
    for i in range(num_groups):
        for j in range(num_inner):
            rfile = open(logdir + '/result.txt')
            r1 = 0
            r5 = 0
    
            count = 0
            curve = [0.0 for k in range(0,5)]
    
            for line in rfile:
                if line == '':
                    continue
                rank = int(line.split(',')[1])
                score = float(line.split(',')[2])
    
                if rank >= 0:
                    rankA = max(rank-1,0)
                    for k in range(rankA,5):
                        curve[k] += 1
    
                count += 1
                if rank == 1 or rank == 0:
                    r1 += 1
    
                if rank <= 5 and rank >= 0:
                    r5 += 1
    
                if rank > 0:
                    ta += 1
                    accScores.append(score)
    
                if rank == 0:
                    tr += 1
                    rejScores.append(score)
    
                if rank == -1:
                    fr += 1
                    accScores.append(score)
    
                if rank == -2:
                    fa += 1
                    rejScores.append(score)
    
            for k in range(len(curve)):
                curve[k] /= count
    
            rank1.append(r1 / float(count))
            rank5.append(r5 / float(count))
            return rank1, rank5, df, curve