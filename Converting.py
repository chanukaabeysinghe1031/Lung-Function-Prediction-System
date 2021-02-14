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

CT_images_dir = "D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train\\"

IMG_PX_SIZE = 50 
NUMBER_OF_SLICES =20
n_classes =1 
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        

def mean(l):
    return  sum(l)/len(l)




CT_images = os.listdir(CT_images_dir)

data_of_patients = pd.read_csv('D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train.csv',index_col=0)

print(data_of_patients.head())

def process_data(patient,labels_df,image_pixel_size=50,number_of_slices=20,visualize=False):
    label = data_of_patients._get_value(patient,'FVC')
    path = CT_images_dir + patient 
    slices = [di.read_file(path+'/'+s) for s in os.listdir(path) ]
    slices.sort(key=lambda x : int(x.ImagePositionPatient[2]))
    print("slices")
    print(len(slices))
    
    
    new_slices = []
    
    slices = [cv2.resize(np.array(each_slice.pixel_array),(IMG_PX_SIZE,IMG_PX_SIZE)) for each_slice in slices]
    chunk_size = math.ceil(len(slices)/NUMBER_OF_SLICES)
    
    print("Chunk size")
    print(chunk_size)
    
    for slice_chunk in chunks(slices,chunk_size):
        slice_chunk = list(map(mean, zip(*slice_chunk)))
        new_slices.append(slice_chunk)
        print(len(new_slices))
        
    print('first slices',len(new_slices))
    if len(new_slices) <NUMBER_OF_SLICES:
        diff = NUMBER_OF_SLICES - len(new_slices)
        for i in range(diff):
            new_slices.append(slice_chunk)
            print('added ',len(new_slices))

    ''' 
   if len(new_slices) == NUMBER_OF_SLICES-1:
        new_slices.append(slice_chunk)
        
    if len(new_slices) == NUMBER_OF_SLICES -2 :
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        
    if len(new_slices) == NUMBER_OF_SLICES-3:
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        
    if len(new_slices) == NUMBER_OF_SLICES -4 :
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        
    if len(new_slices) == NUMBER_OF_SLICES -5 :
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        new_slices.append(slice_chunk)
        '''
    if len(new_slices) == NUMBER_OF_SLICES +2 :
        new_val = list(map(mean, zip(*[new_slices[NUMBER_OF_SLICES-1],new_slices[NUMBER_OF_SLICES]])))
        del new_slices[NUMBER_OF_SLICES]
        new_slices[NUMBER_OF_SLICES-1]=  new_val
        
    if len(new_slices) == NUMBER_OF_SLICES +1 :
        new_val = list(map(mean, zip(*[new_slices[NUMBER_OF_SLICES-1],new_slices[NUMBER_OF_SLICES]])))
        del new_slices[NUMBER_OF_SLICES]
        new_slices[NUMBER_OF_SLICES-1]=  new_val
        
        
    print (patient , len(new_slices))
    
    
    if visualize :
    
        fig = plt.figure()
        
        for num,eachSlice in enumerate(slices) :
            y=fig.add_subplot(5,4,num+1)
            y.imshow(eachSlice)
        plt.show() 

    label = [label[0],label[1]]
    print ("Shape of the new slices ",new_slices[0][0].shape)
    return np.array(new_slices),label


dataset = []

for num , patient in enumerate(CT_images[:1]) :
    #if num%10 ==0 :
            #print(num)
    
    try:
        CT_image,target_value = process_data(patient,data_of_patients,
                                             image_pixel_size=IMG_PX_SIZE,number_of_slices=NUMBER_OF_SLICES)
        dataset.append([CT_image,target_value])
    except  KeyError as e :
        print(e)
    print('=================================')

np.save('dataset-{}-{}-{}.npy'.format(IMG_PX_SIZE,IMG_PX_SIZE,NUMBER_OF_SLICES),dataset)
        

    



        
        