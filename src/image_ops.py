import cv2
import numpy as np
import imageio.v3 as iio

def read_image(path):
    """
    Reads an image (any format) and returns it in RGB format.
    """
    img = iio.imread(path)
    if img is None:
        raise ValueError(f"Could not load image: {path}")
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img

def write_image(path, image):
    """
    Saves an RGB image to disk in BGR (OpenCV) format.
    """
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, bgr)

def convert_to_8bit(image):
    """
    Converts an image to 8-bit range if not already.
    """
    if image.dtype == np.uint8:
        return image
    min_val, max_val = image.min(), image.max()
    if max_val == min_val:
        # Avoid divide-by-zero
        return image.astype(np.uint8)
    scaled = (255 * (image - min_val) / (max_val - min_val)).astype(np.uint8)
    return scaled

def split_channels(image):
    """
    Splits an RGB image into R, G, B single-channel images.
    """
    b, g, r = cv2.split(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    # Convert each channel back to 3-channel for easier display
    r_img = cv2.cvtColor(r, cv2.COLOR_GRAY2RGB)
    g_img = cv2.cvtColor(g, cv2.COLOR_GRAY2RGB)
    b_img = cv2.cvtColor(b, cv2.COLOR_GRAY2RGB)
    return r_img, g_img, b_img

def merge_channels(r_img, g_img, b_img):
    """
    Merges three single-channel R/G/B images into a single RGB image.
    """
    # Each is assumed to be single-channel in a 3-channel structure
    r = cv2.cvtColor(r_img, cv2.COLOR_RGB2GRAY)
    g = cv2.cvtColor(g_img, cv2.COLOR_RGB2GRAY)
    b = cv2.cvtColor(b_img, cv2.COLOR_RGB2GRAY)
    merged_bgr = cv2.merge([b, g, r])
    return cv2.cvtColor(merged_bgr, cv2.COLOR_BGR2RGB)

def make_stack(images, horizontal=True):
    """
    Stacks images horizontally or vertically. 
    They must be the same size. 
    """
    # Convert all to same depth
    processed = []
    for img in images:
        if img.dtype != np.uint8:
            img = convert_to_8bit(img)
        processed.append(img)
    if horizontal:
        return cv2.hconcat(processed)
    else:
        return cv2.vconcat(processed)

def threshold_otsu(image):
    """
    Otsu's threshold on a grayscale version.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)

def threshold_binary(image, thresh_val=127, max_val=255, invert=False):
    """
    Standard binary threshold. If invert=True, uses THRESH_BINARY_INV
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    mode = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    _, result = cv2.threshold(gray, thresh_val, max_val, mode)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)

def adaptive_threshold(image, block_size=11, C=2, method='mean'):
    """
    Adaptive threshold. method='mean' or 'gaussian'.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if method.lower() == 'gaussian':
        ad_type = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    else:
        ad_type = cv2.ADAPTIVE_THRESH_MEAN_C
    result = cv2.adaptiveThreshold(gray, 255, ad_type, 
                                   cv2.THRESH_BINARY, block_size, C)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)

def histogram_equalization(image):
    """
    Histogram Equalization on grayscale, convert back to RGB.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    eq = cv2.equalizeHist(gray)
    return cv2.cvtColor(eq, cv2.COLOR_GRAY2RGB)

def clahe(image, clip_limit=2.0, tile_size=8):
    """
    Contrast Limited Adaptive Histogram Equalization on grayscale.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    clahe_obj = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
    eq = clahe_obj.apply(gray)
    return cv2.cvtColor(eq, cv2.COLOR_GRAY2RGB)
