# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 22:49:45 2021

@author: Chanuka Abeysinghe
"""

import pydicom as di 
import os
from os import listdir
import pylibjpeg
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import math
import tensorflow as tf
import cv2


IMG_PX_SIZE = 50 
NUMBER_OF_SLICES =10

CT_images_dir = "D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\test\\"

patients = os.listdir(CT_images_dir)

data_of_patients = pd.read_csv('D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\test.csv',index_col=0)

image_dataset=[]
label_dataset=[]

def build_dataset(patient):
    
    path = CT_images_dir + patient 
    slices = [di.read_file(path+'/'+s) for s in os.listdir(path) ]
    slices_new=np.array(slices)
    label = data_of_patients._get_value(patient,'FVC')
    
    if(len(slices)==10):
        resized_images=[]
        for image in slices_new:
            #  resizing the (512.512) image into (50,50) image
            resized_image=cv2.resize(np.array(image.pixel_array),(IMG_PX_SIZE,IMG_PX_SIZE)) 
            resized_images.append(resized_image) 
        resized_images = np.transpose(resized_images, (1,2,0))
        image_dataset.append(resized_images)
        label_dataset.append(label)
    else :
        count=0
        patient_folder=0
        remaining_slices=len(slices)
        for slice in range(remaining_slices):
            resized_images=[]
            if(remaining_slices>=10):
                for  slice in range(10) :
                    #  resizing the (512.512) image into (50,50) image
                    resized_image=cv2.resize(np.array(slices[count].pixel_array),(IMG_PX_SIZE,IMG_PX_SIZE))
                    resized_images.append(resized_image)
                    count +=1
                if(len(resized_images)==10):
                    resized_images = np.transpose(resized_images, (1,2,0))
                    image_dataset.append(resized_images)
                    label_dataset.append(label[patient_folder])
                    patient_folder+=1
                remaining_slices -=10
    return slices
    
    
for num , patient in enumerate(patients[:97]) :
    print("Patient : ",patient)
    
    try:
        CT_images_of_the_patient = build_dataset(patient,data_of_patients,
                                             image_pixel_size=IMG_PX_SIZE,number_of_slices=NUMBER_OF_SLICES)
    except  KeyError as e :
        print(e)
        

print(np.array(image_dataset).shape)
print(np.array(label_dataset).shape)
print(len(image_dataset))
print(len(label_dataset))   
np.save('testingdataset-images-{}-{}-{}.npy'.format(NUMBER_OF_SLICES,IMG_PX_SIZE,IMG_PX_SIZE),image_dataset)
np.save('testingdataset-labels.npy',label_dataset)
    
    

    