from __future__ import division
from cv2 import cv2
import numpy as np
import dirhandler as dh
import sys
import os

SIZE = (176,176)

def morpher(img, path=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,5,255,cv2.THRESH_TOZERO)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    kernel2 = np.ones((3,3),np.uint8)
    erosion = cv2.erode(thresh,kernel2,iterations = 1)
    dilation = cv2.dilate(erosion,kernel1,iterations = 7)
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255),2)
    return img

def normalize(img):

    norm_img = np.zeros((img.shape[0], img.shape[1]))
    norm_img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    #img = cv2.normalize(img,None,0,255,cv2.NORM_MINMAX)
    #print(img.shape)
    return norm_img

def rem_lighting(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    smooth = cv2.medianBlur(img, 95)
    division = smooth
    division = cv2.divide(img, smooth, scale=192)
    return division

def greyscale(img, path=False):
    if path:
        img = cv2.imread(img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # blur
    #smooth = cv2.GaussianBlur(gray, (95,95), 0)
    #division = cv2.divide(gray, smooth, scale=192) # divide gray by morphology image
    return gray

def normalize_images(rwlist, overwrite=False):
    normalized_list = []
    for rw in rwlist:
        rd = rw[0]
        wt = rw[1]
        img = cv2.imread(rd)
        #img=rem_lighting(img)
        norm = normalize(img)
        gray = greyscale(norm)
        resize = cv2.resize(gray, SIZE, interpolation=cv2.INTER_NEAREST)
        np.expand_dims(resize, axis=0)
        #normalized_list.append(img)
        if(overwrite):
            cv2.imwrite(wt,resize)
    return normalized_list

def main():  
    # read from ./data/unprocessed and write to ./data/processed
    read_dir = './data/unprocessed/Final_Training_Dataset'
    write_dir = './data/processed/Final_Training_Dataset'
    
    # make sure the write folder exists
    if (not os.path.exists(write_dir)):
        os.makedirs(write_dir)
    readlist = dh.gen_path_list(read_dir)
    rwlist = []
    for rpath in readlist:
        substr = rpath[len(read_dir) + 1 : len(rpath)]
        
        # make sure all the necessary folders exist
        paths = substr.split('/')
        cur, i = write_dir, 0
        while (i < len(paths) - 1):
            cur = os.path.join(cur, paths[i])
            if (not os.path.exists(cur)):
                os.makedirs(cur)
            i += 1
            
        wpath = os.path.join(write_dir, substr)
        rwlist.append((rpath, wpath))
    normalized_list = normalize_images(rwlist, True)
    print('done')    

if __name__ == '__main__':
    main()
