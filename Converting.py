import pydicom as di 
import os
from os import listdir
import gdcm
import pylibjpeg
import pandas as pd 
import matplotlib.pyplot as plt

CT_images_dir = "D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train\\"

CT_images = os.listdir(CT_images_dir)

data_of_patients = pd.read_csv('D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train.csv',index_col=0)

print(data_of_patients.head())

for patient in CT_images[:10]:
    label = data_of_patients._get_value(patient,'FVC')
    path = CT_images_dir + patient 
    slices = [di.read_file(path+'/'+s) for s in os.listdir(path) ]
    slices.sort(key=lambda x : int(x.ImagePositionPatient[2]))
    plt.imshow(slices[0].pixel_array)
    plt.show()    

