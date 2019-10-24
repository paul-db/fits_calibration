## calibration_subs - Fits Standard Calibration Flow
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


# Create Master Dark
import os  
import sys
import numpy as np
import astropy.io.fits as pyfits
from glob import glob

from calibrate_defaults import IMAGES, OUTPUT

def makeDark(Dir, SubDir, median):
    iter = os.listdir(Dir + SubDir)
    darks = np.array([pyfits.getdata(Dir + SubDir + "/%s" % n) for n in iter])
    if darks.size > 0:
        if median == True:
            dark = np.median(darks,axis=0)
        else:
            dark = np.mean(darks,axis=0)
        pyfits.writeto(Dir + "MasterDark.fits", dark,  overwrite=True)
        return dark

def makeFlatDark(Dir, SubDir, median):
    iter = os.listdir(Dir + SubDir)
    flatdarks = np.array([pyfits.getdata(Dir + SubDir + "/%s" % n) for n in iter])
    if flatdarks.size > 0:
        if median == True:
            flatdark = np.median(flatdarks,axis=0)
        else:
            flatdark = np.mean(flatdarks,axis=0)
        return flatdark
    
def makeFlat(Dir, SubDir, Filter, flatdark):
    true_files = []
    iter = os.listdir(Dir + SubDir + "/" + Filter + "/")
    for f in iter:
        if os.path.isfile(Dir + SubDir + "/" +  Filter + "/" + f):
            true_files.append (f)

    Flats = np.array([pyfits.getdata(Dir + SubDir + "/%s" % n) for n in true_files])

    if Flats.size > 0:
        flat = np.median(Flats, axis=0)
        if flatdark is not None:
            flat = (flat - flatdark).clip(min=1)
            
        pyfits.writeto(Dir + "MasterFlat%s.fits"%Filter, flat, overwrite=True)
        return flat

def handleStandardCalibration(path, name, flat, flatratio, dark):
        imagelist = pyfits.open(path + name)
        inhdr = imagelist[0].header
        
        image_data = imagelist[0].data
 
        print(path + name, image_data.shape, end="")

        if dark is not None:
            image_data = image_data - dark
        
        if flat is None:
            if dark is None:
                calib_data = image_data 
            else:
                calib_data = (np.rint(((image_data)).clip(min=0, max=65536))).astype(np.int32)
        else:
            calib_data = (np.rint(((flatratio/flat) * (image_data)).clip(min=0, max=65536))).astype(np.int32)

        outpath = path.replace(IMAGES, OUTPUT) + name
        print (" ==>", outpath)
        # silentfix will fix incorrect N.I.N.A headers
        pyfits.writeto(outpath, calib_data, inhdr, output_verify="silentfix", overwrite=True)
        imagelist.close()
        
