#! /usr/local/bin/python3

'''
This code converts color images to grayscale for use with SealNet.
It creates a copy of the directory passed in as a command-line argument and puts all the 
converted images there.
It expects that the directory passed in has one level of subdirs containing images.
.
└── photos
    ├── 1
    │   ├── 1_1.jpg
    │   ├── 1_2.jpg
    │   └── 1_3.jpg
    └── 2
        ├── 2_1.jpg
        ├── 2_2.jpg
        └── 2_3.jpg

Usage: python3 -d /path/to/photos
Output: ./photos_copy/
'''
import os
from PIL import Image
from argparse import ArgumentParser
from pathlib import Path

def main():
    parser = ArgumentParser(description='Color image to grayscale conversion', add_help=False)
    parser.add_argument('-d', '--directory', dest='directory', action='store',
    type=str, required=True, help='''Directory containing subdirectories that contain photos''')
    settings = parser.parse_args()
    directory = settings.directory
    prefix = Path(directory).resolve()
    copy = str(Path(directory).resolve()) + "_copy"
    if not os.path.exists(copy):
        os.makedirs(copy)

    extensions = ('png', 'jpg', 'jpeg')
    for filename in os.listdir(directory):
        path = os.path.join(prefix, filename)
        if os.path.isdir(path):
            new_path = os.path.join(copy, filename)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            for item in os.listdir(path):
                if item.lower().endswith(extensions):
                    img = Image.open(path + '/' + item).convert('L')
                    img.save(new_path + '/' + item)
        
if __name__ == '__main__':
    main()
