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

#the images should be saved with DAPI/nuclear staining with <filename-1.tif>
#and the transfection channel with <filename-2.tif>
#the "filename" should be the same for both images
#IMPORTANT: MAKE SURE THAT THE FILE NAME DOES NOT HAVE "-" IN IT ANYWHERE,
#EXCEPT AT THE END FOR "-1" AND "-2"

file_list = [f for f in os.listdir('.') if (os.path.isfile(f) and f.split('.')[-1] != 'py')]
print(file_list)
for f in file_list:
	file_name = os.path.splitext(f)[0]
	print(file_name)
	ones = []
	twos = []
	dot_tif = ".tif"
	if file_name.endswith('-1'):
		print("this separated the -1")
		ones.append(file_name)
		print("ones", ones)
		for f in ones:
			join_names = f + dot_tif
			print(join_names)
		chan1 = skimage.io.imread(join_names)
		print("chan1 loaded")
	elif file_name.endswith('-2'):
		print("this separated the -2")
		twos.append(file_name)
		for f in twos:
			join_names = f + dot_tif
			print(join_names)
		chan2 = skimage.io.imread(join_names)
		print(chan2)
		print("twos", twos)
	print("Images loaded")
	
#for f in file_list:

	## NORMALIZE THE GREYSCALE IMAGES
	#good practice to normalize the pixel values so that each pixel value has a value between 0 and 1

def normalize_chan(chan):
	pixels = asarray(chan)
	pixels = pixels.astype('float32') #make integers floats
		#normalize to range of 0-1
	pixels /= pixels.max()
	return pixels

norm_chan1 = normalize_chan(chan1)
norm_chan2 = normalize_chan(chan2)
print("Images normalized")

	## DETERMINE THE THRESHOLD WITH AUTOMATIC THRESHOLDING

thresh_val_chan1 = skimage.filters.thresholding.threshold_otsu(norm_chan1)
thresh_val_chan2 = skimage.filters.thresholding.threshold_otsu(norm_chan2)
thresh_chan1 = norm_chan1 > thresh_val_chan1 #> used because imaged cells are lighter than background
thresh_chan2 = norm_chan2 > thresh_val_chan2
print("Images thresholded")	

		## COUNT PARTICLES

		# Label each individual cell 
im_lab1, num_obj1 = skimage.measure.label(thresh_chan1, return_num=True)
im_lab2, num_obj2 = skimage.measure.label(thresh_chan2, return_num=True)
print("Particles counted")

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
auto_filter_particles_num(thresh_chan2, num_obj2, im_lab2)
print("Particles filtered")

	## FIND TRANSFECITON EFFICIENCY RATIO

number_cells_chan1 = auto_filter_particles_num(thresh_chan1, num_obj1, im_lab1)
number_cells_chan2 = auto_filter_particles_num(thresh_chan2, num_obj2, im_lab2)
Transfection_ratio = (number_cells_chan2)/(number_cells_chan1)*100 
print("The transfection ratio is", Transfection_ratio)

	## SAVE THE OUTPUT AS A CSV FILE

df = pd.DataFrame([[file_name,number_cells_chan1,number_cells_chan2,Transfection_ratio]],columns=['file_name','number_cells_chan1','number_cells_chan2','Transfection_ratio'])
df.to_csv('transfection_effeciency.csv', mode='a+')
print("data saved")