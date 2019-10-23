#!/usr/bin/env python

## build_calibration_tree - Build Folder Structure for Calibration Flow
## Copyright (C) 2019 Paul de Backer
##
## This file is part of fits_calibration
##
## fits_calibration is free software: you can redistribute it and/or modify
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
import argparse

from calibrate_defaults import *
def MakeAdir (path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.args[0] != 17: 
            print ("Creation of the directory %s failed" % path)



parser = argparse.ArgumentParser(description='Process Calibration Tree')
parser.add_argument('-filter', nargs='+', help='Create Filter Folders')

args = parser.parse_args()

MakeAdir(FLAT)
MakeAdir(DARK)
MakeAdir(FLATDARK)
MakeAdir(OUTPUT)
MakeAdir(IMAGES)
if args.filter is not None:
    for f in args.filter:
        MakeAdir(FLAT + "/" +f)
        MakeAdir(IMAGES + "/" +f)
        MakeAdir(OUTPUT + "/" + f)
