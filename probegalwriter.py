
import os 
from pathlib import Path
import random

def create_splits(directory, databuild):
    """Create training and testing split according to num_splits

    Args:
        directory (string): the path to the photo directory
        num_splits (int): number of splits or cross-fold validation
        
    Returns:
        list[list]: list[i] is another list for each {i+1}_th split. 
                    list[i] = [num of training photos, number of unique seals for training, number of probe photos, number of gallery photos, number of unique seals for testing]
    """
    splits_dir = os.path.join(os.path.expanduser('./splits'))

    if not os.path.isdir(splits_dir):  
        os.makedirs(splits_dir)
    individuals = get_individuals(directory)
    labels = list(individuals.keys())
    num_label_testing = len(labels)//4
    num_label_training = len(individuals) - num_label_testing
    
    splitData = []
    for i in range(num_label_testing):
        random.shuffle(labels)
        probeCount, galleryCount = create_testing_set(individuals, labels[:num_label_testing], i+1)
        trainingCount = create_training_set(individuals, labels[num_label_testing:], i+1)
        splitData.append([trainingCount, num_label_training, probeCount, galleryCount, num_label_testing])
        
    return splitData
    

def write_training_set(photopaths, counter):
    """Create a training set (train.txt file) in the splits folder. 
       The training file will be in the form:
       Total_Number_Of_Labels X
       PATH_TO_PHOTO1 LABEL
       PATH_TO_PHOTO2 LABEL
       ...

    Args:
        individuals (dictionary): map seal class to lists of file path to each of that seal's photo
        labels (list): list of the corresponding labels
        counter (int): current number of training - 1
        
    Returns:
        int: number of training images
    """
    fname = './splits/split{}/train.txt'.format(counter)
    
    trainingCount = 0
    with open(fname, 'w') as f:
        f.write('Total_Number_Of_Labels ' + str(len(individuals)) + '\n')
        for key in labels:
            for v in individuals[key]:
                f.write(v + ' ' + key + '\n')
                trainingCount += 1
                
    return trainingCount
                
    
def create_testing_set(individuals, labels, counter):
    """Create probe and gallery for testing, probe has one photo for each individual and gallery has the remaining photos

    Args:
        individuals (dictionary): map seal class to lists of file path to each of that seal's photo
        labels (list): list of the corresponding labels
        counter (int): current number of training - 1

    Returns:
        (int, int): number of probe and gallery images
    """
    splits_dir = os.path.join(os.path.expanduser('./splits/split{}/fold_1/'.format(counter)))
    if not os.path.isdir(splits_dir):
        os.makedirs(splits_dir)

    gallery = open('./splits/split{}/gal.txt'.format(counter),'w')
    probe = open('./splits/split{}/probe.txt'.format(counter),'w')
    
    probeCount, galleryCount = 0, 0
    
    for key in labels:
        value = individuals[key]
        temp = value[::]
        random.shuffle(temp)
        probe.write(temp[0]+ ' ' + key + '\n')
        probeCount += 1
        for j in range(1, len(value)):
            gallery.write(temp[j] + ' ' + key + '\n')
            galleryCount += 1
        
    gallery.close()
    probe.close()
    
    return probeCount, galleryCount


def get_individuals(directory):
    prefix = str(Path(directory).resolve())
    extensions = ('png', 'jpg', 'jpeg')
    individuals = {}
    assert(os.path.exists(str(prefix)))

    for item in os.listdir(str(prefix)):
        path = os.path.join(prefix, item)
        if not os.path.isdir(path):
            continue
        name = str(int(item)-1)
        individuals[name] = []
        for file_name in os.listdir(path):
            if file_name.lower().endswith(extensions):
                file_path = os.path.join(path, file_name)
                individuals[name].append(str(file_path))
    
    return individuals
