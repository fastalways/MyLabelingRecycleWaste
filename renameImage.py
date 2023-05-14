import os
import glob

## -------------- CONFIG HERE ---------------------
DIR = "E:/eieie/"
ALLOW_IMAGE_TYPE = ['txt']
## ------------------------------------------------


filenames = []
imagenames = []
for IMAGE_TYPE in ALLOW_IMAGE_TYPE:
    filenames.append(glob.glob(DIR+"*."+IMAGE_TYPE))
    print(f"{IMAGE_TYPE} has {len(filenames[len(filenames)-1])}.")
for names in filenames :
    for name in names:
        imagenames.append(name) 
imagenames.sort()
if(len(imagenames)>0):
    imgpath = os.path.split(imagenames[0])[0]
    split_path=imgpath.split('/')
    if(len(split_path)==1):
        split_path=imgpath.split('\\')
    if(len(split_path)==1):
        split_path=imgpath.split("//")
    folderName = split_path[len(split_path)-1]
    print(f"Rename to -> {folderName}")
    print(f"Examples of renamed files : ")
    for count,imagename in enumerate(imagenames):
        imgpath = os.path.split(imagename)[0]
        imgname = os.path.split(imagename)[1]
        file_extension = os.path.splitext(imgname)[1]
        newname = folderName + "_" + str(count+1).zfill(5) + file_extension
        print(imgpath+"/"+newname)
        if count == 4:
            break
    # Confirmation
    all_images_count = len(imagenames)
    print(f"ALL Image = {all_images_count}")
    confFlag = input("Confirm to rename? (y/n) ")
    if(confFlag=='y' or confFlag=='Y'):
        for count,imagename in enumerate(imagenames):
            imgpath = os.path.split(imagename)[0]
            imgname = os.path.split(imagename)[1]
            file_extension = os.path.splitext(imgname)[1]
            newname = folderName + "_" + str(count+1).zfill(5) + file_extension
            os.rename(imagename,imgpath+'/'+newname)
            if count%49==0:
                print(f"{count+1}/{all_images_count}")
        print("Done!")
else:
    print(f"no image type {ALLOW_IMAGE_TYPE} in {DIR}")
