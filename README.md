# Analyzing Transfection Efficiency

This repository contains files helpful for determining transfection efficiency for cells! 

One file is a Jupyter notebook file with instructions in markdown blocks on how to manually load and determine transfection efficiency. In this code, you will manually determine the threshold for your cells with a histogram.

The other two files are python scripts which can be used to run similar code to that seen in the Jupyter notebook on images to automatically determine transfection efficiency. These scripts work by being called on in a command line through: "python <script name?.py". The thresholding is done automatically in these scripts with the Otsu method, but could be changed in the code if another method is preferred. The .py file named "transfection_efficiency_one" can be run on an image in a folder that has been split into the DAPI channel with a -1 file suffix and the transfection channel as a -2 file suffix. The numbers of cells counted and the trasnfection ratio are saved to a csv file. The .py file named "transfection_efficiency_multiple", was my best attempt at getting the code to run on multiple images in a folder with the DAPI and transfected channels signified as -1 and -2. I could not get this code to iterate through all files in the folder properly, I encountered errors where it would try to compare the channels from two different images. I uploaded this file anyways because I'm sure with some tweaks from people who know more coding than I do that the problems can be fixed! 

I hope this code is helpful, and can let you determine your transfection efficiency either in a fun and interactive way with Jupyter notebook or quickly on the command line! :)
