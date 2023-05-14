import os, os.path

# simple version for working with CWD
#print len([name for name in os.listdir('.') if os.path.isfile(name)])

# path joining version for other paths
DIR = './RecycleWasteDatasetCropped/'
for name_folder in os.listdir(DIR):
    if os.path.isdir(os.path.join(DIR, name_folder)):
        print(name_folder,len([name for name in os.listdir(DIR+name_folder) if os.path.isfile(os.path.join(DIR+name_folder, name))]))