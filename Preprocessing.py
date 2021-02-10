import pydicom
import matplotlib.pyplot as plt
import scipy.misc
import pandas as pd
import numpy as np
import os
import imageio
id= "ID00009637202177434476278\\"
path = os.chdir("D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train\\ID00336637202286801879145\\")

#i =1
#for file in os.listdir(path):
    #new_file_name ="ID00426637202313170790466_{}.dcm".format(i)
    #os.rename(file,new_file_name)
    #i=i+1
    
#Get all picture names
c=[]
names=os.listdir (path) #path
#Separate the file name in the folder from the .dcm behind
for name in names:
    index=name.rfind (".")
    name=name [:index]
    c.append (name)
for files in c:
    picture_path="D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train\\ID00336637202286801879145\\"+files+".dcm"
    out_path="D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train_new\\ID00010637202177584971671\\"+files+".jpg"
    ds=pydicom.read_file (picture_path)
    img=ds.pixel_array #extract image information
    print(img)
print ("all is changed")