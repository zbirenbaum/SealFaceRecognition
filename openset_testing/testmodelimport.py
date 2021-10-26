import os

def get_model_dirs(model_dir):
    modelslist = []
    for model in os.listdir(model_dir):
        modelslist.append(os.path.join(model_dir, model))
    if len(modelslist) == 0:
        exit(1)
    return modelslist

model_dir = './models/'
config_file = '../config.py'

modelslist = get_model_dirs(model_dir)  
print(modelslist)
model_name = modelslist[0]
