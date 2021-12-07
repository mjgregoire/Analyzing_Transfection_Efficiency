# Analyzing Transfection Efficiency

This repository contains files helpful for determining transfection efficiency for cells! 

Both files are designed to analyze transfeciton efficiency so long as the images have been split into the DAPI channel with a -1 file suffix and the transfection channel as a -2 file suffix AND the images are single z-slices. The images should be the only files in a folder which may also contain the script.

One file is a Jupyter notebook file with instructions in markdown blocks on how to manually load and determine transfection efficiency one image at a time. In this code, you will manually determine the threshold for your cells with a histogram.

The other file is a python script which contains similar code to that seen in the Jupyter notebook and can be run on multiple images to automatically determine transfection efficiency. This script works by being called on in a command line through: "python transfection_efficiency.py". The thresholding is done automatically with the Otsu method, but could be changed in the code if another method is preferred. The numbers of the total cells counted in channel 1, the cells counted in channel 2, the transfection ratio, and transfection efficiency (as a percent) are saved to a csv file titled "transfection_efficiency.csv". 

I hope these codes are helpful, and can let you determine your transfection efficiency either in a fun and interactive way with Jupyter notebook or quickly on the command line! :)
