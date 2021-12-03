import dirhandler as dh
import os

#photodirs_all = dh.get_photo_dirs(path='final_dataset/processed', exclude=1)

entries = os.listdir(str('final_dataset/processed'))
print(len(entries))
