import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
from os import listdir,mkdir
from os.path import isfile, join, exists
import copy
import re


'''  Label Listing  '''
label_name_list = [
    'Paper',
]

save_img_extension = 'jpg' # jpg png bmp ....
dataset_path = 'D:/RecycleWasteDataset/test/Paper/CardboardBox/'
dataset_output_crop_path = 'D:/RecycleWasteDatasetCropped/test/Paper/CardboardBox/'
img_path = dataset_path + '/'
img_crop_path = dataset_output_crop_path + '/'
paddingVertical = 0
paddingHorizontal = 0
countingList = [1] * len(label_name_list)

class cvRect:
    def __init__(self, xywh):
        self.x = xywh[0]
        self.y = xywh[1]
        self.w = xywh[2]
        self.h = xywh[3]
        self.xmin = self.x
        self.ymin = self.y
        self.xmax = self.x + self.w
        self.ymax = self.y + self.h
    def area(self):
        return self.w * self.h
    def tl(self):
        return [self.x,self.y]
    def br(self):
        return [self.x+self.w,self.y+self.h]
    def center(self):
        return [self.x+(self.w//2),self.y+(self.h//2)]
    def xywh(self):
        return  [self.x,self.y,self.w,self.h]


def loadLabelsFromFile(txt_path):
    xywhs = []
    labels = []
    if os.path.exists(txt_path): # เช็คว่า path existed ?
        with open(txt_path) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            xywh_strs = [re.split(r'\t+', line) for line in lines]
            for xywh_str in xywh_strs:
                if(len(xywh_str)==5):
                    (xc,yc,wc,hc) = int(xywh_str[1]),int(xywh_str[2]),int(xywh_str[3]),int(xywh_str[4])
                    labels.append(xywh_str[0])
                    xywhs.append(cvRect([xc,yc,wc,hc]))
    return xywhs,labels

def ProcessInEachFolder():
    global img_path,img_crop_path,object_name,paddingVertical,paddingHorizontal
    list_files = []
    list_files = [f for f in listdir(img_path) if isfile(join(img_path, f))]
    del_lists = []
    for i,fname in enumerate(list_files):
        last = len(fname) - 1
        file_ext = fname[-4:]
        if(file_ext!='anno'):
            del_lists.append(fname) # mark as delete
            #print(file_ext)
    for val in del_lists:
        list_files.remove(val)
    print(f"Listing label_anno_files file ext:{list_files}")
    # Process cropped_images in anno_list
    for i,fname in enumerate(list_files):
        single_image_path = ''
        single_image_name = img_path+fname
        single_image_name = single_image_name[0:len(single_image_name)-5]
        single_image_path_jpg = single_image_name + '.jpg'
        single_image_path_png = single_image_name + '.png'
        single_image_path_JPG_BIG = single_image_name + '.JPG'
        if(os.path.isfile(single_image_path_jpg)):
            single_image_path = single_image_path_jpg
        elif (os.path.isfile(single_image_path_png)):
            single_image_path = single_image_path_png
        elif (os.path.isfile(single_image_path_JPG_BIG)):
            single_image_path = single_image_path_JPG_BIG
        else :
            print(f'Cannot found image : {single_image_name}')
            continue # if not found images
        cropping_img = cv.imread(single_image_path)
        xywhs,labels = loadLabelsFromFile(img_path+fname)
        (h_cropping_img,w_cropping_img) = cropping_img.shape[:2]
        for idx,xyhw in enumerate(xywhs):
            label = labels[idx]
            id_label = label_name_list.index(label)
            # crop
            save_crop_image_path = dataset_output_crop_path + '/' + label + '/' + label + '_' + str(countingList[id_label]).zfill(5) + '.' + save_img_extension
            newPadded = cvRect([xyhw.x-paddingHorizontal,xyhw.y-paddingVertical,xyhw.w+(paddingHorizontal*2),xyhw.h+(paddingVertical*2)])
            #check valid
            padding_valid = True
            if(newPadded.x<=0 or newPadded.y<=0):
                padding_valid = False
            if(newPadded.w>w_cropping_img or newPadded.h>h_cropping_img):
                padding_valid = False
            cropped_image = None
            if(padding_valid):
                cropped_image = cropping_img[newPadded.y:newPadded.y+newPadded.h, newPadded.x:newPadded.x+newPadded.w]
            else:
                cropped_image = cropping_img[xyhw.y:xyhw.y+xyhw.h, xyhw.x:xyhw.x+xyhw.w]
            #print(save_crop_image_path)
            if((cropped_image!=None).any()):
                if save_img_extension == 'jpg':
                    cv.imwrite(save_crop_image_path,cropped_image,[int(cv.IMWRITE_JPEG_QUALITY), 100])
                else :
                    cv.imwrite(save_crop_image_path,cropped_image)
            else:
                print(f'Error: cropping in {single_image_path} [{xyhw.x},{xyhw.y},{xyhw.w},{xyhw.h}] skipped {save_crop_image_path}')
            countingList[id_label] = countingList[id_label] + 1 # increase counter

def main():
    global object_name,img_path,img_crop_path,dataset_path,dataset_output_crop_path,label_name_list
    for name in label_name_list:
        object_name = name
        img_crop_path = dataset_output_crop_path + '/' + object_name + '/'
        if not os.path.exists(img_crop_path): # เช็คว่า path existed ?
            os.mkdir(img_crop_path)
    print(f'Processing in Folder : {dataset_path}')
    img_path = dataset_path + '/'
    ProcessInEachFolder()
    print('------------------------------Finished---------------------------------')


if __name__ == "__main__":
    main()