import cv2
import numpy as np

def gaussian_blur(image, ksize=3, sigma=0.0):
    """
    Applies Gaussian Blur to an RGB image.
    """
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(image, (ksize, ksize), sigma)

def median_filter(image, ksize=3):
    """
    Applies a Median Filter to an RGB image.
    """
    if ksize % 2 == 0:
        ksize += 1
    return cv2.medianBlur(image, ksize)

def bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """
    Bilateral filter for edge-preserving smoothing.
    """
    # OpenCV expects BGR, so convert temporarily:
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    filtered = cv2.bilateralFilter(bgr, d, sigma_color, sigma_space)
    return cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)

def canny_edge(image, threshold1=100, threshold2=200):
    """
    Canny edge detection on an RGB image. Returns single-channel edges as RGB.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, threshold1, threshold2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

def sobel_edge(image, dx=1, dy=0, ksize=3):
    """
    Applies Sobel edge detection. dx or dy can be 1 or 0 to detect horizontal/vertical.
    ksize must be odd, up to 31.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    sobel = cv2.Sobel(gray, cv2.CV_64F, dx, dy, ksize=ksize)
    # Convert scale, then back to RGB
    abs_sobel = cv2.convertScaleAbs(sobel)
    return cv2.cvtColor(abs_sobel, cv2.COLOR_GRAY2RGB)

def laplacian_edge(image, ksize=3):
    """
    Laplacian edge detection on an RGB image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
    abs_lap = cv2.convertScaleAbs(lap)
    return cv2.cvtColor(abs_lap, cv2.COLOR_GRAY2RGB)

def unsharp_mask(image, ksize=5, alpha=1.5):
    """
    Simple unsharp masking. alpha is the strength of the sharpening.
    """
    blur = cv2.GaussianBlur(image, (ksize, ksize), 0)
    # sharpened = original + alpha*(original - blurred)
    sharpened = cv2.addWeighted(image, 1 + alpha, blur, -alpha, 0)
    return sharpened

def gamma_correction(image, gamma=1.0):
    """
    Applies gamma correction to the RGB image.
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)

def brightness_contrast(image, alpha=1.0, beta=0):
    """
    Adjusts brightness and contrast:
      new_image = alpha*image + beta
    alpha: contrast (1.0 = no change)
    beta: brightness (0 = no change)
    """
    # Convert to float to avoid clipping
    new = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return new

def invert_image(image):
    """
    Inverts (255 - pixel) for each channel.
    """
    return 255 - image
