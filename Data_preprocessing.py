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

CT_images_dir = "D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train\\"

patients = os.listdir(CT_images_dir)

data_of_patients = pd.read_csv('D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train.csv',index_col=0)

image_dataset=[]
label_dataset=[]

def build_dataset(patient,labels_df,image_pixel_size=50,number_of_slices=20,visualize=False):
    
    path = CT_images_dir + patient 
    slices = [di.read_file(path+'/'+s) for s in os.listdir(path) ]
    #print(slices)
    slices_new=np.array(slices)
    
    if(len(slices)==10):
        resized_images=[]
        for image in slices_new:
            #  resizing the (512.512) image into (50,50) image
            resized_image=cv2.resize(np.array(image.pixel_array),(IMG_PX_SIZE,IMG_PX_SIZE)) 
            print("shape of the ct image",resized_image.shape)
            resized_images.append(resized_image)
        resized_images = np.transpose(resized_images, (1,2,0))
        image_dataset.append(resized_images)
    else : 
        count=0
        remaining_slices=len(slices)
        for slice in range(remaining_slices):
            resized_images=[]
            if(remaining_slices>=10):
                for  slice in range(10) :
                    #  resizing the (512.512) image into (50,50) image
                    resized_image=cv2.resize(np.array(slices[count].pixel_array),(IMG_PX_SIZE,IMG_PX_SIZE))
                    print("shape of the ct image",resized_image.shape)
                    resized_images.append(resized_image)
                    count +=1
                if(len(resized_images)==10):
                    resized_images = np.transpose(resized_images, (1,2,0))
                    image_dataset.append(resized_images)
                print(len(image_dataset))
                remaining_slices -=10
    return slices 
    
    
for num , patient in enumerate(patients[:45]) :
    if num%10 ==0 :
            print("Patient : ",num)
    
    try:
        CT_images_of_the_patient = build_dataset(patient,data_of_patients,
                                             image_pixel_size=IMG_PX_SIZE,number_of_slices=NUMBER_OF_SLICES)
        #dataset.append([CT_image,target_value])
    except  KeyError as e :
        print(e)
        
    print('=================================')

image_dataset2=np.array(image_dataset)
print(np.array(image_dataset).shape)
print(image_dataset[0].shape)    
    
    
    

    