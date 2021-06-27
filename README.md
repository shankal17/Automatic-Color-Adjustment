# Automatic-Color-Adjustment

Automatic color balancing algorithm. Rumor has it this is very similar to Photoshop's process. On the left is the original image, and to the right is the processed image

![Green Color Cast](/Results/girl_color_balance.JPG)

## Getting Started

Once you have the code, set up a virtual environment if you would like and install the necessary libraries by running the command below.
```bat
pip install -r /path/to/requirements.txt
```
Then, in [RGB_histogram.py](https://github.com/shankal17/Automatic-Color-Adjustment/blob/main/Scripts/RGB_histogram.py#:~:text=if%20__name__%20%3D%3D%20%27__main__,processed%2C%20scale%3D20) change the following lines to process and display your own images!

```py
if __name__ == '__main__':

    img, processed = color_correct('path/to/original/image', threshold=1.5)
    display_side_by_side(img, processed, scale=20)
```

# My Results

For each image, the left is the original image, and the right is the processed image

![Tag Shot](/Results/tag_color_balanced.JPG)

![Bad Color Cast](/Results/dude_with_strong_color_cast.JPG)

![Girl In Mall](/Results/girl_in_mall_color_balance.JPG)


