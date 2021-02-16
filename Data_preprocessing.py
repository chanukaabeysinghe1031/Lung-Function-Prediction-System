# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 22:49:45 2021

@author: Chanuka Abeysinghe
"""

import pydicom as di 
import os
from os import listdir
import gdcm
import pylibjpeg
import pandas as pd 
import matplotlib.pyplot as plt
import cv2 
import numpy as np
import math
import tensorflow as tf


IMG_PX_SIZE = 50 
NUMBER_OF_SLICES =10

CT_images_dir = "D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train\\"

patients = os.listdir(CT_images_dir)

data_of_patients = pd.read_csv('D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train.csv',index_col=0)

dataset=[]

def build_dataset(patient,labels_df,image_pixel_size=50,number_of_slices=20,visualize=False):
    
    path = CT_images_dir + patient 
    slices = [di.read_file(path+'/'+s) for s in os.listdir(path) ]
    #print(slices)
    slices_new=np.array(slices)
    
    if(len(slices)==10):
        print("Shape of the slices",slices_new.shape)
        dataset.append(np.array(slices_new))
    else : 
        count=0
        remaining_slices=len(slices)
        for slice in range(remaining_slices):
            new_slices10=[]
            if(remaining_slices>=10):
                for  slice in range(10) :
                    new_slices10.append(slices[count])
                    count +=1
                if(len(new_slices10)==10):
                    dataset.append(np.array(new_slices10))
                print(len(dataset))
                remaining_slices -=10
    return slices 
    
    
for num , patient in enumerate(patients) :
    if num%10 ==0 :
            print("Patient : ",num)
    
    try:
        CT_images_of_the_patient = build_dataset(patient,data_of_patients,
                                             image_pixel_size=IMG_PX_SIZE,number_of_slices=NUMBER_OF_SLICES)
        #dataset.append([CT_image,target_value])
    except  KeyError as e :
        print(e)
        
    print('=================================')

print(np.array(dataset).shape())
    
    
    
    
    
    