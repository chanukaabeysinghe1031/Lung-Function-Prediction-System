# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 09:34:12 2021

@author: Chanuka Abeysinghe
"""

# import the necessary packages
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import glob
import cv2
import os
def load_CT_attributes(inputPath):
	# initialize the list of column names in the CSV file and then
	# load it using Pandas
	cols = ["Patient", "Weeks", "FVC", "Percent", "Age","Sex","SmokingStatus"]
	df = pd.read_csv(inputPath, sep=" ", header=None, names=cols)
	# return the data frame
	return df

def process_CT_attributes(df, train, test):
	# initialize the column names of the continuous data
	continuous = ["Percent", "Age","Weeks"]
	# performin min-max scaling each continuous feature column to
	# the range [0, 1]
	cs = MinMaxScaler()
	trainContinuous = cs.fit_transform(train[continuous])
	testContinuous = cs.transform(test[continuous])
    # one-hot encode the zip code categorical data (by definition of
	# one-hot encoing, all output features are now in the range [0, 1])
	zipBinarizer = LabelBinarizer().fit(df["SmokingStatus"])
	trainCategorical = zipBinarizer.transform(train["SmokingStatus"])
	testCategorical = zipBinarizer.transform(test["SmokingStatus"])
	# construct our training and testing data points by concatenating
	# the categorical features with the continuous features
	trainX = np.hstack([trainCategorical, trainContinuous])
	testX = np.hstack([testCategorical, testContinuous])
	# return the concatenated training and testing data
	return (trainX, testX)