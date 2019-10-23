# fits_calibration

Calibrates  FITS Astronomy Images according to the Standar Calibration protocol using Lights, Darks, Flats and FlatDarks.
Calibrated images are written to the Calibrated folder in fits format (BITPIX=16).

For a calibratrion use the following steps from the command line:

**Step 1: Create and switch to an empty folder**
Create the necessary folder structure with build_calibration_tree.py
For images taken with different filters, generate also a subfolder per filter with the -filter option
```
python path_to_install_folder/build_calibration_tree.py -h

usage: build_calibration_tree.py [-h] [-filter FILTER [FILTER ...]]

Process Calibration Tree

optional arguments:
  -h, --help            show this help message and exit
  -filter FILTER [FILTER ...]
                        Create Filter Folders
```                        
**Step 2: Copy your images to the folder structure**

Science Images go to the Lights folder
Darks to the Darks Folder
Flats to the Flats Folder
Flat Darks to the FlatDarks Folder

(for images with different color filter move the files to the corresponding filter directory, do not forget flats per filter)

**Step 3: Run the calibration**
```
python path_to_install_folder/standard_calibration.py
```
for a list of all options
```
python path_to_install_folder/standard_calibration.py -h

usage: standard_calibration.py [-h] [-median] [-nodarks] [-nodarkflats]
                               [-noflats] [-d DIR]

optional arguments:
  -h, --help         show this help message and exit
  -median            Use median dark and darkflats instead of mean
  -nodarks           Process without dark files
  -nodarkflats       Process without dark flats
  -noflats           Process without flats
  -d DIR, --dir DIR  Image root directory
  
  ```

Calilbrated images ar written to the Calibrated folder structure
