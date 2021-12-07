#!/usr/bin/env python 
"""
Created December 2021

@author: mjgregoire
"""

## BEGIN BY LOADING THE MODULES

import os
import shutil
from pathlib import Path

#standard modules
import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
import csv
import pandas as pd

#for image processing
import scipy
from scipy import stats	
import skimage
import skimage.io
import skimage.exposure
import skimage.measure	
import skimage.filters
import skimage.morphology
from skimage.morphology import reconstruction
import PIL	
from PIL import Image

## LOAD THE IMAGE/S

#IMPORTANT: MAKE SURE THE ONLY FILES IN YOUR FOLDER ARE THIS SCRIPT AND THE IMAGES

#the images should be saved with DAPI/nuclear staining with <filename-1.tif>
#and the transfection channel with <filename-2.tif>
#the "filename" should be the same for both images
#IMPORTANT: MAKE SURE THAT THE FILE NAME DOES NOT HAVE "-" IN IT ANYWHERE,
#EXCEPT AT THE END FOR "-1" AND "-2"

file_list = [f for f in os.listdir('.') if (os.path.isfile(f) and f.split('.')[-1] != 'py')]
print(file_list)

## LOAD THE ONES FIRST

for f in file_list:
	file_name = os.path.splitext(f)[0]
	#print(file_name)
	#print(file_name[-1])
	ones = []
	dot_tif = ".tif"
	if file_name[-1] == '1':
		print("this separated the -1")
		ones.append(file_name)
		print("ones", ones)
		file_name_short = file_name[:12]
		print("short is", file_name_short)
		for f in ones:
			join_names = f + dot_tif
			print(join_names)
			chan1 = skimage.io.imread(join_names)
			print("chan1 images loaded")
	
			## NORMALIZE THE GREYSCALE IMAGES
			#good practice to normalize the pixel values so that each pixel value has a value between 0 and 1

			def normalize_chan(chan):
				pixels = asarray(chan)
				pixels = pixels.astype('float32') #make integers floats
				#normalize to range of 0-1
				pixels /= pixels.max()
				return pixels

			norm_chan1 = normalize_chan(chan1)
			print("Chan1 Images normalized")

			## DETERMINE THE THRESHOLD WITH AUTOMATIC THRESHOLDING

			thresh_val_chan1 = skimage.filters.thresholding.threshold_otsu(norm_chan1)
			thresh_chan1 = norm_chan1 > thresh_val_chan1 #> used because imaged cells are lighter than background
			print("Chan1 Images thresholded")	

			## COUNT PARTICLES

			# Label each individual cell 
			im_lab1, num_obj1 = skimage.measure.label(thresh_chan1, return_num=True)
			print("Chan1 Particles counted")

			## FIND THE AREAS OF THE CELLS, auto filter bottom 10% out (small particles)

			# Convert pixels to physical units 
			#ip_dist stands for inter-pixel distance. It is unique to each camera!
			ip_dist_63x = 0.1036339 # In units of microns per pixel , Leica DMi8 has 103 nm interpixel distance at 63x magnification
			#minus_magnification = 0.1036339*63 # to find out the value for the camera alone, multiply by the magnification
			#ip_dist_10x =  minus_magnification / 10 #this will tell you the pixel distance for 10x magnifcation

			def auto_filter_particles_num(thresh_chan, num_obj, im_lab):
				approved_cells = np.zeros_like(thresh_chan) #make empty image same size as threshold image
				for i in range(num_obj):
        				cell = (im_lab == i + 1) #grabs "cells" one by one
        				cell_area = np.sum(cell) * ip_dist_63x**2
        				percent_cell_area =  cell_area/100
        				if (percent_cell_area > 0.1): #any value greater than a 10% of cell area
            					approved_cells += cell #add the cells that make the cutoff to the empty image
				approved_lab, num_obj = skimage.measure.label(approved_cells, return_num=True)
				x = num_obj
				return x

			auto_filter_particles_num(thresh_chan1, num_obj1, im_lab1)
			print("Chan1 Particles filtered")

			## SAVE CELLS TO VARIABLE 

			number_cells_chan1 = auto_filter_particles_num(thresh_chan1, num_obj1, im_lab1)
			print("Chan1 cells saved")

			df1 = pd.DataFrame([[file_name_short,number_cells_chan1]], columns=['file_name','number_cells_chan1'])
			print("this is df1", df1)
			df1.to_csv('chan1.csv', mode='a+')
			print("made chan1 csv")

## DO THE SAME THING FOR CHANNEL 2

for f in file_list:
	file_name2 = os.path.splitext(f)[0]
	#print(file_name)
	#print(file_name[-1])
	twos = []
	dot_tif = ".tif"
	if file_name2[-1] == '2':
		print("this separated the -2")
		twos.append(file_name2)
		print("twos", twos)
		file_name_short = file_name[:12]
		print("short is", file_name_short)
		for f in twos:
			join_names = f + dot_tif
			print(join_names)
			chan2 = skimage.io.imread(join_names)
			print("chan 2 Images loaded")

			def normalize_chan(chan):
				pixels = asarray(chan)
				pixels = pixels.astype('float32') #make integers floats
				pixels /= pixels.max()
				return pixels

			norm_chan2 = normalize_chan(chan2)
			print("Chan2 Images normalized")

			thresh_val_chan2 = skimage.filters.thresholding.threshold_otsu(norm_chan2)
			thresh_chan2 = norm_chan2 > thresh_val_chan2
			print("Chan2 Images thresholded")

			im_lab2, num_obj2 = skimage.measure.label(thresh_chan2, return_num=True)
			print("Chan2 Particles counted")
	
			ip_dist_63x = 0.1036339
			def auto_filter_particles_num(thresh_chan, num_obj, im_lab):
				approved_cells = np.zeros_like(thresh_chan) #make empty image same size as threshold image
				for i in range(num_obj):
        				cell = (im_lab == i + 1) #grabs "cells" one by one
        				cell_area = np.sum(cell) * ip_dist_63x**2
        				percent_cell_area =  cell_area/100
        				if (percent_cell_area > 0.1): #any value greater than a 10% of cell area
            					approved_cells += cell #add the cells that make the cutoff to the empty image
				approved_lab, num_obj = skimage.measure.label(approved_cells, return_num=True)
				x = num_obj
				return x

			auto_filter_particles_num(thresh_chan2, num_obj2, im_lab2)
			print("Chan2 Particles filtered")

			number_cells_chan2 = auto_filter_particles_num(thresh_chan2, num_obj2, im_lab2)
			print("Chan2 cells saved")
		
			df2 = pd.DataFrame([[file_name_short,number_cells_chan2]], columns=['file_name','number_cells_chan2'])
			print("this is df2", df2)
			df2.to_csv('chan2.csv', mode='a+')
			print("made chan2 csv")
	

## ADD THE CHANNEL DFS TOGETHER AND SAVE THE OUTPUT AS A CSV FILE 

df_chan1 = pd.read_csv('chan1.csv')
df_chan2 = pd.read_csv('chan2.csv')
df = pd.concat([df_chan1, df_chan2], axis=1, join="inner")
print("this is the raw data", df)
df = df.drop_duplicates()
df = df.drop(labels = 1, axis = 0)
df = df.drop(df.columns[[4]], axis = 1)
df = df.drop(df.filter(regex='Unnamed').columns, axis=1)
df = df.fillna(0)
df['number_cells_chan1'] = pd.to_numeric(df['number_cells_chan1'], errors='coerce').fillna(0).astype(int)
df['number_cells_chan2'] = pd.to_numeric(df['number_cells_chan2'], errors='coerce').fillna(0).astype(int)
print(df)
df['transfection_ratio'] = df['number_cells_chan2']/df['number_cells_chan1']
df['transfection_efficiency'] = df['transfection_ratio']*100
print("added transfection ratio!", df)

df.to_csv('transfection_effeciency.csv', mode='a+')
print("data saved")
