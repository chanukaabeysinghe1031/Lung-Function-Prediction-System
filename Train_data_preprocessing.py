# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 22:49:45 2021

@author: Chanuka Abeysinghe
"""

import pydicom as di
import os

import pandas as pd
import numpy as np
import cv2



CT_images_dir = "D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\train\\"

patients = os.listdir(CT_images_dir)

data_of_patients = pd.read_csv('D:\\IIT\\4th year\\FYP\\Lung Fibrosis\\Model\\Dataset\\trainData.csv', index_col=0)

image_dataset = []
attributes_dataset = []
label_dataset = []

IMG_PX_SIZE = 50
NUMBER_OF_SLICES = 10

def build_dataset(patient, labels_df, image_pixel_size=50, number_of_slices=20, visualize=False):
    path = CT_images_dir + patient
    slices = [di.read_file(path + '/' + s) for s in os.listdir(path)]
    slices_new = np.array(slices)

    label = data_of_patients._get_value(patient, 'FVC')
    week = data_of_patients._get_value(patient, 'Weeks')
    percentage = data_of_patients._get_value(patient, 'Percent')
    gender = data_of_patients._get_value(patient, 'Sex')
    smoking_status = data_of_patients._get_value(patient, 'SmokingStatus')
    age = data_of_patients._get_value(patient, 'Age')

    if (len(slices) == 10 or (len(slices) > 10 and len(slices) < 20)):
        resized_images = []
        attributes = []
        for image in slices_new:
            #  resizing the (512.512) image into (50,50) image
            resized_image = cv2.resize(np.array(image.pixel_array), (IMG_PX_SIZE, IMG_PX_SIZE))
            resized_images.append(resized_image)
        resized_images = np.transpose(resized_images, (1, 2, 0))
        image_dataset.append(resized_images)
        label_dataset.append(label)
        attributes.append(week)
        attributes.append(percentage)
        attributes.append(age)
        attributes.append(gender)
        attributes.append(smoking_status)
        attributes_dataset.append(attributes)

        print("shape of dataset", np.array(image_dataset).shape)
    else:
        count = 0
        patient_folder = 0
        remaining_slices = len(slices)
        for slice in range(remaining_slices):
            resized_images = []
            attributes = []
            if (remaining_slices >= 10):
                for slice in range(10):
                    #  resizing the (512.512) image into (50,50) image
                    resized_image = cv2.resize(np.array(slices[count].pixel_array), (IMG_PX_SIZE, IMG_PX_SIZE))
                    # print("shape of the ct image",resized_image.shape)
                    resized_images.append(resized_image)
                    count += 1
                if (len(resized_images) == 10):
                    resized_images = np.transpose(resized_images, (1, 2, 0))
                    image_dataset.append(resized_images)
                    label_dataset.append(label[patient_folder])
                    attributes.append(week[patient_folder])
                    attributes.append(percentage[patient_folder])
                    attributes.append(age[patient_folder])
                    attributes.append(gender[patient_folder])
                    attributes.append(smoking_status[patient_folder])
                    attributes_dataset.append(attributes)
                    patient_folder += 1
                print(len(image_dataset))
                remaining_slices -= 10
                print("shape of dataset", np.array(image_dataset).shape)
    return slices


for num, patient in enumerate(patients):
    # if num%10 ==0 :
    print("Patient : ", patient)

    try:
        CT_images_of_the_patient = build_dataset(patient, data_of_patients,
                                                 image_pixel_size=IMG_PX_SIZE, number_of_slices=NUMBER_OF_SLICES)
        # dataset.append([CT_image,target_value])
    except  KeyError as e:
        print(e)

    # print('=================================')

# image_dataset2=np.array(image_dataset)
print(np.array(image_dataset).shape)
print(np.array(label_dataset).shape)
print(np.array(attributes_dataset).shape)

# print(image_dataset[3])
# print(np.array(image_dataset[0][0]).shape)
print(len(image_dataset))
print(len(label_dataset))
np.save('dataset-images4.npy', image_dataset)
np.save('dataset-labels4.npy', label_dataset)
np.save('dataset-attributes4.npy', attributes_dataset)


