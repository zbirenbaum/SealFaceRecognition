#! /usr/local/bin/python3

'''
 Gets a directory and outputs file names and individual names for use in splits
 Assumes each subdir contains only one individual, and the name of the subdir is the name of the individual
 Image extensions are expected, append to the tuple below to extend
'''

import os 
import sys
from pathlib import Path


def get_individuals(directory):
    """
    Usually used on photo folder. 
    Return a dictionary whose [key, pair] = [name_of_subfolder, list_of_path_to_each_photos_within_the_subfolder]

    :type directory: String
    """

    prefix = Path(directory).resolve()
    extensions = ('png', 'jpg', 'jpeg')
    individuals = {}
    assert(os.path.exists(prefix))

    for item in os.listdir(prefix):
        path = os.path.join(prefix, item)
        if not os.path.isdir(path):
            continue
        name = str(item)
        individuals[name] = []
        for file_name in os.listdir(path):
            if file_name.lower().endswith(extensions):
                file_path = os.path.join(path, file_name)
                individuals[name].append(str(file_path))
    
    return individuals

def main():
    args = sys.argv
    if len(args) != 3:
        print('Usage: python format_data.py GALLERY/PROBE DIRECTORY')
        print('Ex: python format_data.py GALLERY ../photos')
        return
    directory = args[2]
    
    #gallery: facechips that will be used as reference
    if (args[1].lower() == 'gallery'):
        individuals = get_individuals(directory)
        labels = list(individuals.keys())
        with open('./referencePhotos.txt', 'w') as gallery:
            for key in labels:
                value = individuals[key]
                for j in range(len(value)):
                    gallery.write(value[j] + ' ' + key + '\n')

    #probe: facechips that will be used to compare with the reference photos
    elif (args[1].lower() == 'probe'):
        with open('./probePhotos.txt', 'w') as probe: 
            path = Path(directory).resolve()
            extensions = ('png', 'jpg', 'jpeg')
            assert(os.path.exists(path))

            for file_name in os.listdir(path):
                if file_name.lower().endswith(extensions):
                    file_path = os.path.join(path, file_name)
                    probe.write((str(file_path)) + ' 1\n')
    else:
        print("First argument must be 'gallery' or 'probe'")
        return



if __name__ == "__main__":
    main()
