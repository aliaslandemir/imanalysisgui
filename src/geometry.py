import cv2
import numpy as np

def rotate(image, angle=90):
    """
    Rotates an RGB image by 'angle' degrees about its center.
    Positive angles -> counter-clockwise.
    """
    h, w, _ = image.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def flip(image, flip_code=0):
    """
    flip_code: 0 -> flip vertically, 1 -> flip horizontally, -1 -> flip both
    """
    flipped = cv2.flip(image, flip_code)
    return flipped

def resize(image, width=None, height=None):
    """
    Resizes maintaining aspect ratio if only one dimension is provided.
    """
    h, w, _ = image.shape
    if width is None and height is None:
        return image
    if width is None:
        # scale by height
        ratio = height / float(h)
        width = int(w * ratio)
    elif height is None:
        # scale by width
        ratio = width / float(w)
        height = int(h * ratio)
    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized

def crop(image, x, y, w, h):
    """
    Crops a region from x,y to x+w, y+h. 
    Make sure it doesn't exceed the image boundaries.
    """
    H, W, _ = image.shape
    x2 = min(x + w, W)
    y2 = min(y + h, H)
    return image[y:y2, x:x2]
