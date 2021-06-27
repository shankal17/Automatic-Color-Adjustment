"""Classes and functions needed to perform auto color correction

Functions
---------
create_lookup(black_point, white_point, gray_point=False)
    Creates lookup table of color transformation curve
color_correct(img_path, threshold=1)
    Performs color correction on an image
display_side_by_side(img1, img2, scale=100, title="Default Title")
    Displays a window with img1 and img2 side-by-side
"""

import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

def create_lookup(black_point, white_point, gray_point=False):
    """Creates lookup table of color transformation curve

    Parameters
    ----------
    black_point : int
        Black point of color channel
    white_point : int
        White point of color channel
    gray_point : int
        Gray point of color channel
    
    Returns
    -------
    numpy.array
        Resulting lookup table
    """

    if gray_point:
        interp = interp1d([black_point, gray_point[0], white_point], [0, gray_point[1], 255], kind='quadratic')
    else:
        interp = interp1d([black_point, white_point], [0, 255])

    table = np.zeros(256)

    for i in range(256):
        if i < black_point:
            table[i] = 0
        elif i > white_point:
            table[i] = 255
        else:
            table[i] = interp(i)
    return table

def color_correct(img_path, threshold=1):
    """Performs color correction on an image

    Parameters
    ----------
    img_path : string
        Path to the image to be operated on
    threshold : float, optional
        Percentage of pixels to saturate

    Returns
    -------
    numpy.array
        Original image
    numpy.array
        Processed image
    """

    img = cv2.imread(img_path)
    if img is None:
        sys.exit("Could not read the image.")
    shape = img.shape
    size = shape[0]*shape[1]
    actual_thresh = size*threshold/100

    color = ('b','g','r')
    curves = []
    for i in range(3):
        histr = cv2.calcHist([img], [i], None, [256], [0,256])
        black_point = 0
    
        # Find black point
        for c, elem in enumerate(np.cumsum(histr)):
            if elem > actual_thresh:
                black_point = c
                break
            
        # Find white point
        histr = np.flip(histr)
        for c, elem in enumerate(np.cumsum(histr)):
            if elem > actual_thresh:
                white_point = 255-c
                break

        curves.append(create_lookup(black_point, white_point))

    # plt.show()
    processed = np.zeros_like(img)
    blue, green, red = cv2.split(img)
    processed[:, :, 0] = curves[0][blue]
    processed[:, :, 1] = curves[1][green]
    processed[:, :, 2] = curves[2][red]

    return img, processed

def display_side_by_side(img1, img2, scale=100, title="Default Title"):
    """Displays a window with img1 and img2 side-by-side

    Parameters
    ----------
    img1 : numpy.array
        First image to be displayed
    img2 : numpy.array
        Second image to be displayed
    scale : float, optional
        Scale, in percentage, to resize the images
    title : string, optional
        Title of the display
    """

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.axis("off")
    ax2.axis("off")
    ax1.title.set_text("Original")
    ax2.title.set_text("Processed")
    combined = np.concatenate((img, processed), axis=1)
    width = int(combined.shape[1]*scale/100)
    height = int(combined.shape[0]*scale/100)
    dim = (width, height)
    combined = cv2.resize(combined, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow(title, combined)
    cv2.waitKey()

if __name__ == '__main__':

    img, processed = color_correct('path/to/original/image', threshold=1.5)
    display_side_by_side(img, processed, scale=20)

