import json
import shutil
import os
import pathlib


def create_dirs(fold):
    os.makedirs("facenet/"+fold+"/train")
    os.makedirs("facenet/"+fold+"/test")

def data_path_substr(fullpath):
    return fullpath[fullpath.rfind('/', 0, fullpath.rfind('/')):len(fullpath)]

def copy_files():
    base_path = "splitsave/"
    for fold in os.listdir(base_path):
        trainpath = base_path + fold + "/train.json"
        testpath = base_path + fold + "/test.json"

        
        trainfp = open(trainpath)
        testfp = open(testpath)
        traindata = json.load(trainfp)
        testdata = json.load(testfp)
        trainfp.close()
        testfp.close()

        newtraindir = "facenet/"+fold+"/train"
        newtestdir = "facenet/"+fold+"/test"
        try:
            os.makedirs(newtraindir)
            os.makedirs(newtestdir)
        except:
            pass
        
        for dir in traindata.keys():
            copypath = newtraindir + data_path_substr(dir)
            try:
                os.makedirs(copypath)
            except:
                pass
            for file in traindata[dir]:
                shutil.copy2(file, copypath) 
        print("copied training")
        for dir in testdata.keys():
            copypath = newtestdir + data_path_substr(dir)
            try:
                os.makedirs(copypath)
            except:
                pass
            for file in testdata[dir]:
                shutil.copy2(file, copypath) 
        print("copied testing")
            #os.makedirs(newtraindir+"/"+)
copy_files()
