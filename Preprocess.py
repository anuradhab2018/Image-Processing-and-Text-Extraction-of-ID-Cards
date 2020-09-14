import cv2
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
import matplotlib.image as mpimg
import numpy as np
import os

output_dir = 'C:/Users/DELL/Desktop/Maveai/Images/Residentcard/Preprocessed/combined'


# Preporcessing Steps
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


# ===========================================================

# Get_string function
def get_string(DIR, filename):
    # Read image using opencv
    print(filename)
    image = cv2.imread(DIR + "/" + filename)

    gray = get_grayscale(image)
    skewed = deskew(gray)

    # Resizing of the images
    # print('Original Dimensions : ',image.shape)
    scale_percent = 100  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(skewed, dim, interpolation=cv2.INTER_AREA)
    # print('Resized Dimensions : ',resized.shape)

    # Extract the file name without the file extension
    newfile_name = filename.split('.')[0]

    # Create a directory for outputs
    output_dir = 'C:/Users/DELL/Desktop/Maveai/Images/Residentcard/Preprocessed'

    # Save the filtered image in the output directory
    save_path = os.path.join(output_dir, newfile_name + "_filter.jpg")
    cv2.imwrite(save_path, resized)
    return output_dir + '/' + newfile_name + "_filter.jpg"


# ===========================================================
def get_concat_v_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=False):
    if im1.width == im2.width:
        _im1 = im1
        _im2 = im2
    elif (((im1.width > im2.width) and resize_big_image) or
          ((im1.width < im2.width) and not resize_big_image)):
        _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)
    dst = Image.new('RGB', (_im1.width, _im1.height + _im2.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (0, _im1.height))
    return dst

DIR = 'C:/Users/DELL/Desktop/Maveai/Images/Residentcard'
images_list = []
for filename in sorted(os.listdir(DIR)):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        A = get_string(DIR, filename)
        images_list.append(A)

name = "img.jpg"

imgs = [Image.open(i) for i in images_list]

newimg = get_concat_v_resize(imgs[0], imgs[1])
newimg.save(output_dir + '/' + name)

[os.remove(i) for i in images_list]