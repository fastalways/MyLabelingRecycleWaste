import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
from os import listdir
from os.path import isfile, join, exists
import re
import copy

from numpy.lib.shape_base import split
DIRs = ["./RecycleWasteDataset/"] # TrainSet
DIR_to_save = "./RecycleWasteDatasetYolo/data/train/"



SAVE_IMAGE_EXTENSION = "png"
TEST_MODE = False # True->write on disk False->only testing
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
        return [self.x+(self.w/2),self.y+(self.h/2)]
    def get_xywh(self):
        return  [self.x,self.y,self.w,self.h]

dictLabel = {
    'glass':0,
    'metal':1,
    'paper':2,
    'plastic':3,
}
def makeLabelYOLO(xywh,nameClass,IMAGE_WIDTH,IMAGE_HEIGHT):
    ''' makeLabelYOLO(xywh<-cvRect,nameClass<-string,IMAGE_SIZE<-numpy.shape())
    '''
    # Yolo Format
    ''' Label_ID X_CENTER_NORM Y_CENTER_NORM WIDTH_NORM HEIGHT_NORM Label_ID_2 X_CENTER_NORM
    X_CENTER_NORM = X_CENTER_ABS/IMAGE_WIDTH 
    Y_CENTER_NORM = Y_CENTER_ABS/IMAGE_HEIGHT 
    WIDTH_NORM = WIDTH_OF_LABEL_ABS/IMAGE_WIDTH 
    HEIGHT_NORM = HEIGHT_OF_LABEL_ABS/IMAGE_HEIGHT
    '''
    global cvRect,dictLabel
    # find Label_ID
    Label_ID = dictLabel[nameClass]
    X_CENTER_NORM = xywh.center()[0]/IMAGE_WIDTH 
    Y_CENTER_NORM = xywh.center()[1]/IMAGE_HEIGHT 
    WIDTH_NORM = xywh.w/IMAGE_WIDTH 
    HEIGHT_NORM = xywh.h/IMAGE_HEIGHT
    return "%d %.6f %.6f %.6f %.6f" % (Label_ID,X_CENTER_NORM,Y_CENTER_NORM,WIDTH_NORM,HEIGHT_NORM)


def main():
    numIMG = 0
    global DIRs,DIR_to_save,SAVE_IMAGE_EXTENSION
    # Create classes.txt
    path_classes_txt = DIR_to_save+'classes.txt'
    if not os.path.exists(path_classes_txt):
        classesFile = open(path_classes_txt, "a+")
        print("classes.txt not exits -> writing... "+path_classes_txt)
        for key in dictLabel:
            n = classesFile.write(key+'\n')
            print(f"->{key}")
        classesFile.close()
    # Read GLabel *.anno file
    for DIR in DIRs: # access in each path (DIR)
        print(f"Enter to process in  -------->  {DIR}")
        for name_folder in os.listdir(DIR): # access each image/label in a path (DIR)
            print(f'Working in {name_folder}')
            if os.path.isdir(os.path.join(DIR, name_folder)):
                for name in os.listdir(DIR+name_folder): ## in each folder
                    #print(f'Working in {name}')
                    if os.path.isfile(os.path.join(DIR+name_folder, name)):
                        full_filename = os.path.join(DIR+name_folder, name)
                        filename, file_extension = os.path.splitext(full_filename)
                        fname = os.path.splitext(os.path.basename(full_filename))[0]
                        if(file_extension=='.anno'):
                            if os.path.exists(full_filename): # path existed ?
                                ## find image
                                found_image = False
                                aImagePath = ""
                                prefixImagePath = filename
                                jpgImagePath = prefixImagePath + '.jpg'
                                #print(jpgImagePath)
                                if os.path.exists(jpgImagePath):
                                    aImagePath = jpgImagePath
                                    found_image = True
                                JPGImagePath = prefixImagePath + '.JPG'
                                if os.path.exists(JPGImagePath):
                                    aImagePath = JPGImagePath
                                    found_image = True
                                pngImagePath = prefixImagePath + '.png'
                                if os.path.exists(pngImagePath):
                                    aImagePath = pngImagePath
                                    found_image = True
                                if(found_image):
                                    IMG = cv.imread(aImagePath)
                                    if IMG is not None :
                                        (heightIMG,widthIMG,_) = IMG.shape
                                        numSTR = "_" + str(numIMG).zfill(5) 
                                        abs_path_to_save = DIR_to_save+'/'+fname+numSTR
                                        #print(abs_path_to_save+'.'+SAVE_IMAGE_EXTENSION)
                                        if(not TEST_MODE):
                                            cv.imwrite(abs_path_to_save+'.'+SAVE_IMAGE_EXTENSION,IMG)
                                        numIMG += 1
                                        # open txt (GLabel) file
                                        with open(full_filename) as file:
                                            write_text = ''
                                            lines = file.readlines()
                                            countLine = 0
                                            for line in lines:
                                                countLine += 1
                                                xywh_str = re.split(r'\t+', line)
                                                if(len(xywh_str)==5):
                                                    if(xywh_str[0] in dictLabel):
                                                        try:
                                                            xPos=int(xywh_str[1])
                                                            yPos=int(xywh_str[2])
                                                            wPos=int(xywh_str[3])
                                                            hPos=int(xywh_str[4])
                                                            xywh = cvRect([xPos,yPos,wPos,hPos])
                                                            yolo_label_oneline = makeLabelYOLO(xywh,xywh_str[0],widthIMG,heightIMG)
                                                            write_text+=yolo_label_oneline+'\n'
                                                        except:
                                                            print("Couldn't convert x,y,w,h(string) to number(int) !!!")
                                                            print(f"Pls check at {full_filename} in line {countLine}")
                                                            print(f"{xywh_str[0]}-{xywh_str[1]}-{xywh_str[2]}-{xywh_str[3]}-{xywh_str[4]}")
                                                    else :
                                                        print(f"Unknow Label {xywh_str[0]} : in line {countLine} at {full_filename}, pls add label to dictLabel variable")
                                                        print(f"{xywh_str[0]}-{xywh_str[1]}-{xywh_str[2]}-{xywh_str[3]}-{xywh_str[4]}")
                                                else:
                                                    print(f'txt pos error in {full_filename}')
                                                    print(f"{xywh_str[0]}-{xywh_str[1]}-{xywh_str[2]}-{xywh_str[3]}-{xywh_str[4]}")
                                            ### write yolo label .txt
                                            if(not TEST_MODE):
                                                f = open(abs_path_to_save+'.txt', "w")
                                                f.write(write_text)
                                                f.close()
                                    else :
                                        print("Couldn't open image !!! (support: JPG/jpg/png)")
                                        print(f"Pls check at {os.path.join(DIR+name_folder+'/'+name, '.jpg')}")
                                else :
                                    print("Couldn't find image !!! (support: JPG/jpg/png)")
                                    print(f"Pls check at {full_filename}")
    print("Finished!!!!")



if __name__ == "__main__":
    main()