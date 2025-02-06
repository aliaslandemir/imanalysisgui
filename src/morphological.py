import cv2
import numpy as np

def erode(image, kernel_size=3, iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    eroded = cv2.erode(bgr, kernel, iterations=iterations)
    return cv2.cvtColor(eroded, cv2.COLOR_BGR2RGB)

def dilate(image, kernel_size=3, iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    dilated = cv2.dilate(bgr, kernel, iterations=iterations)
    return cv2.cvtColor(dilated, cv2.COLOR_BGR2RGB)

def open_morph(image, kernel_size=3):
    """
    Morphological opening = erode -> dilate
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    opened = cv2.morphologyEx(bgr, cv2.MORPH_OPEN, kernel)
    return cv2.cvtColor(opened, cv2.COLOR_BGR2RGB)

def close_morph(image, kernel_size=3):
    """
    Morphological closing = dilate -> erode
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    closed = cv2.morphologyEx(bgr, cv2.MORPH_CLOSE, kernel)
    return cv2.cvtColor(closed, cv2.COLOR_BGR2RGB)

def gradient_morph(image, kernel_size=3):
    """
    Morphological gradient = dilate - erode
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    grad = cv2.morphologyEx(bgr, cv2.MORPH_GRADIENT, kernel)
    return cv2.cvtColor(grad, cv2.COLOR_BGR2RGB)

def tophat_morph(image, kernel_size=3):
    """
    Top-hat = image - open(image)
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    top = cv2.morphologyEx(bgr, cv2.MORPH_TOPHAT, kernel)
    return cv2.cvtColor(top, cv2.COLOR_BGR2RGB)

def blackhat_morph(image, kernel_size=3):
    """
    Black-hat = close(image) - image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    black = cv2.morphologyEx(bgr, cv2.MORPH_BLACKHAT, kernel)
    return cv2.cvtColor(black, cv2.COLOR_BGR2RGB)
