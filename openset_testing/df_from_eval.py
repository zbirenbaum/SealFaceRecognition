import copy
from load_mean_features import save_eval, load_eval
import os
from six import iteritems
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import sys
import inspect
import pandas as pd
from seenbefore_save_folds import run_eval
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

try:
    best_by_fold_by_model = load_eval("final")
except:
    best_by_fold_by_model = run_eval(["SealNet", "PrimNet"]).copy()
    save_eval(best_by_fold_by_model, "final")

def get_diff_df(result_dict):
    comparison_df_list = []
    result_dict['Difference']=result_dict['SealNet']-result_dict['PrimNet']
    comparison_df = pd.concat(result_dict.values(), axis=0, keys=result_dict.keys())
    comparison_df = comparison_df.reindex(['SealNet', 'PrimNet', 'Difference'], level=0)
    comparison_df_list.append(comparison_df)
    for i in range(len(comparison_df_list)):
        print("Fold " + str(i) + ":")
        print(comparison_df_list[i])
def format_dict(target):
    new = copy.deepcopy(target)
    new5 = copy.deepcopy(target)
    for k,v in iteritems(target):
        for k2, best in iteritems(v):
            new[k][k2]=best.to_dict().copy()
            new5[k][k2]=best.r5.to_dict().copy()
    return new, new5

def make_fulldf(data):
    dflist = []
    for _, v in iteritems(data):
        df = pd.DataFrame.from_dict(v).T
        df.loc['MEAN'] = df.mean()
        df.loc['SD'] = df.std()
        df = df.drop([1,2,3,4,5])
        dflist.append(df)
    fulldf = pd.concat({'SealNet': dflist[0], 'PrimNet': dflist[1], 'Difference': dflist[0]-dflist[1]})
    fulldf = fulldf.drop(('Difference', 'SD'))
    return fulldf

r1_best_by_fold_by_model, r5_best_by_fold_by_model = format_dict(best_by_fold_by_model)
r1 = make_fulldf(r1_best_by_fold_by_model)
r5 = make_fulldf(r5_best_by_fold_by_model)
comparison_df = pd.concat({"R1": r1, "R5": r5})
comparison_df = comparison_df.swaplevel(i=0, j=1)
comparison_df = comparison_df.reindex(['SealNet', 'PrimNet', 'Difference'], level=0)
comparison_df.index.names = ["1% FAR", "Rank", ""]
print(comparison_df)
