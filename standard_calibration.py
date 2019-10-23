#!/usr/bin/env python

## standard_calibration - Fits Standard Calibration Flow
## Copyright (C) 2019 Paul de Backer
##
## This file is part of fits_calibration
##
### fits_calibration is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## fits_calibration is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with fits_calibration.  If not, see <http://www.gnu.org/licenses/>.



import os  
import sys
#import argparse
import numpy as np
#import astropy.io.fits as pyfits
from argparse import ArgumentParser
from glob import glob

from calibrate_defaults import *
from calibrate_subs import *



# Main program start

parser = ArgumentParser()
parser.add_argument("-median", action='store_true', help='Use median dark and darkflats instead of mean')
parser.add_argument("-nodarks", action='store_true', help='Process without dark files')
parser.add_argument("-nodarkflats", action='store_true', help='Process without dark flats')
parser.add_argument("-noflats", action='store_true', help='Process without flats')
parser.add_argument("-d", "--dir",  help='Image root directory')


args = parser.parse_args()
         
if args.dir != None:
    INPUT = args.dir + "/"
else:
    INPUT = "./"
    

if args.nodarks == False:
    dark_data = makeDark(INPUT, DARK, args.median)
else:
    dark_data = None

if dark_data is None:
    print ("No Darks")
    
if args.nodarkflats == False:
    flat_dark_data = makeFlatDark (INPUT, FLATDARK, args.median)
else:
    flat_dark_data = None

if flat_dark_data is None:
    print ("No Dark Flats")


IMAGE_DIR = INPUT + IMAGES
for root, dirs, files in os.walk(IMAGE_DIR):
    parts = os.path.split(root)
    pix_val = 0
    if args.noflats == False:
        flat_data = makeFlat(INPUT + FLAT + parts[1].strip() + "/",  parts[1].strip(), flat_dark_data)
        if flat_data is not None:
            x_center = (int) (flat_data.shape[0] / 2)
            y_center = (int) (flat_data.shape[1] / 2)
            pix_val = np.mean (flat_data[x_center-50:x_center+50, y_center-50:y_center+50])
    else:
        flat_data = None

    if flat_data is None:
        print ("No Flats")
        
    iter = os.listdir(root)
    for name in iter:
       if os.path.isfile(root + "/" + name):             
            handleStandardCalibration(root + "/", name, flat_data, pix_val, dark_data)

 
