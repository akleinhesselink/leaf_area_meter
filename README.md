# Leaf Area Meter

Leaf area meter is a python script for measuring leaf area from flatbed scanner 

## Installation

Download leaf_area.py and put in the directory with leaf images. 

## Usage

First create an CSV file with 8 arguments separated by commas. See "arg_file.csv" for an example. 

1. Image file pattern -- file pattern to find image files 
2. Resolution of images in dpi 
3. Minimum object size in px. Any objects smaller than this size will be filtered out of the results.  Use to filter out dust etc. 
4. topcrop: number of pixels to crop off top of image 
5. botcrop: number of pixels to crop off bottom of image
6. lcrop: number of pixels to crop off left of image 
7. rcrop: number of pixels to crop off right of image 

Then run the script from the shell like this: 
```bash
./leaf_area.py arg_file.csv  
```
*Where "arg_file.csv" is the name of your CSV file with arguments. 

## Contributing


## License
[CC0](https://choosealicense.com/licenses/gpl-3.0/)