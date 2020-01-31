#!/usr/bin/env python
# coding: utf-8

# In[283]:


### Work in Progress. I modified the working version to use stacks


# In[284]:


import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as mpimg
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from scipy import ndimage as ndi
import skimage.util as util
import skimage.io as io 
import skimage.util as u
import glob
from os import path 
import pandas as pd 
import re
import sys
from matplotlib.backends.backend_pdf import PdfPages


# In[285]:


def calc_px_per_cm2( resolution ): 
    return(np.int( (resolution**2)/(2.54**2)))
    
def find_leaves( binary_img, min_size ): 
    labels,__ = ndi.label(binary_img)
    items, area = np.unique(labels, return_counts = True)
    big_items = items[ area > min_size ][1:] # subtract background 
    leaf = np.isin( labels, big_items )      # keep items that are leaf 
    item_areas = area [ np.isin(items, big_items ) ] 
    return( leaf, item_areas )

def make_summary_table( img_files, NumLeaves, TotalArea, AvgArea, PercArea = '', Mean = ''): 
    d = {'Slice': [path.splitext(f)[0] for f in img_files]}
    my_dat = pd.DataFrame(data = d)
    my_dat['Count'] = NumLeaves
    my_dat['Total Area'] = TotalArea
    my_dat['Average Size'] = AvgArea
    my_dat['%Area'] = PercArea
    my_dat['Mean'] = Mean
    return(my_dat)

def plot_leaf_area(filename, leaf, leaf_area ): 
    
    fig, axes = plt.subplots(1, 2, figsize=(10,10))
    ax = axes.ravel()
    ax[0].imshow(mpimg.imread(filename), cmap = plt.cm.gray)
    ax[0].set_title(filename)
    ax[1].imshow(leaf, cmap=plt.cm.binary)
    ax[1].set_title( "Tota leaf area: {:.2f} cm\N{SUPERSCRIPT TWO}".format(leaf_area)  )
    fig.tight_layout()  
    plt.close()
    return(fig)
    

def main(): 
        
    if( len( sys.argv ) == 2 ):
        arg_file = sys.argv[1]
        print("using csv arguments in: " + arg_file)
        # parameters from argfile 
        pattern, resolution, min_size, topcrop, botcrop, lcrop, rcrop = ( pd.read_csv(arg_file, header = None).iloc[0] ) 
    else: 
        print("incorrect number of arguments")
        
    px_per_cm2 = calc_px_per_cm2(resolution)
        
    img_files = glob.glob(pattern)
    img_files = np.sort( img_files)
    imgs = io.imread_collection(img_files)
    img_stack = np.stack( [rgb2gray(x) for x in imgs ])

    img_size = img_stack.shape[1:  ]
    d1 = np.int_( [0, img_size[0]] ) + np.int_([topcrop, - botcrop])
    d2 = np.int_( [0, img_size[1]] ) + np.int_([rcrop, - lcrop ])
    img_stack = img_stack[ : , d1[0]:d1[1], d2[0]:d2[1]] # crop 
    
    # make binary 
    thresh = np.int_( np.array( [threshold_otsu( x ) for x in img_stack] ).mean())
    binary = np.array( [ x < thresh for x in img_stack ] )
    binary = np.array( [ clear_border(x) for x in binary] )
    
    # find leaves and save stats 
    out = [ find_leaves( x, min_size ) for x in binary ]
    leaves = np.stack( [ x[0] for x in out ])
    item_areas = np.array( [x[1] for x in out ])

    # calculate particle statistics 
    NumLeaves = np.int_( [ len(x) for x in item_areas]  )
    AvgArea = np.array( [ np.mean(x) for x in item_areas ] )/px_per_cm2
    TotalArea = np.array([ np.sum(x) for x in item_areas ] )/px_per_cm2 
    
    print( "Saving leaf areas")
    my_dat = make_summary_table( img_files, NumLeaves, TotalArea, AvgArea )
    scan_group = re.search( '^([A-Za-z0-9_-]+)\\*', pattern).group(1)    
    my_dat.to_csv( scan_group + '_leaf_area.csv', index= False)
    
    results = list( zip( img_files, leaves, TotalArea) )
    
    # save images to check cropping and leaf detection 
    print( "Plotting pdf to check results")
    pp = PdfPages(scan_group + '_check.pdf' )
    figs = [plot_leaf_area(x[0], x[1], x[2] ) for x in results ]
    [pp.savefig(x, dpi = 150) for x in figs ]
    pp.close()
    


# In[286]:


if __name__== "__main__":
  main()

