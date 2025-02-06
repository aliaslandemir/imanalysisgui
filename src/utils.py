from typing import Callable, Dict, Any

# We import from local modules
from .filters import (
    gaussian_blur, median_filter, bilateral_filter,
    canny_edge, sobel_edge, laplacian_edge, unsharp_mask,
    gamma_correction, brightness_contrast, invert_image
)
from .morphological import (
    erode, dilate, open_morph, close_morph,
    gradient_morph, tophat_morph, blackhat_morph
)
from .image_ops import (
    threshold_binary, threshold_otsu, adaptive_threshold,
    histogram_equalization, clahe
)
from .geometry import rotate, flip, resize, crop

# Example: A dictionary that maps filter/operation names to (function, parameter-info).
# We keep param-info minimal for demonstration; you can expand to define param types/ranges.
FILTERS_MAP: Dict[str, Dict[str, Any]] = {
    "Gaussian Blur": {
        "function": gaussian_blur,
        "params": [
            {"name": "ksize", "type": "int", "default": 3, "min": 1, "max": 31},
            {"name": "sigma", "type": "float", "default": 0.0, "min": 0.0, "max": 10.0}
        ]
    },
    "Median Filter": {
        "function": median_filter,
        "params": [
            {"name": "ksize", "type": "int", "default": 3, "min": 1, "max": 31}
        ]
    },
    "Bilateral Filter": {
        "function": bilateral_filter,
        "params": [
            {"name": "d", "type": "int", "default": 9, "min": 1, "max": 100},
            {"name": "sigma_color", "type": "int", "default": 75, "min": 1, "max": 200},
            {"name": "sigma_space", "type": "int", "default": 75, "min": 1, "max": 200},
        ]
    },
    "Canny Edge": {
        "function": canny_edge,
        "params": [
            {"name": "threshold1", "type": "int", "default": 100, "min": 0, "max": 255},
            {"name": "threshold2", "type": "int", "default": 200, "min": 0, "max": 255}
        ]
    },
    "Sobel Edge": {
        "function": sobel_edge,
        "params": [
            {"name": "dx", "type": "int", "default": 1, "min": 0, "max": 1},
            {"name": "dy", "type": "int", "default": 0, "min": 0, "max": 1},
            {"name": "ksize", "type": "int", "default": 3, "min": 1, "max": 31}
        ]
    },
    "Laplacian Edge": {
        "function": laplacian_edge,
        "params": [
            {"name": "ksize", "type": "int", "default": 3, "min": 1, "max": 31}
        ]
    },
    "Unsharp Mask": {
        "function": unsharp_mask,
        "params": [
            {"name": "ksize", "type": "int", "default": 5, "min": 1, "max": 31},
            {"name": "alpha", "type": "float", "default": 1.5, "min": 0.0, "max": 5.0}
        ]
    },
    "Gamma Correction": {
        "function": gamma_correction,
        "params": [
            {"name": "gamma", "type": "float", "default": 1.0, "min": 0.1, "max": 5.0}
        ]
    },
    "Brightness/Contrast": {
        "function": brightness_contrast,
        "params": [
            {"name": "alpha", "type": "float", "default": 1.0, "min": 0.0, "max": 5.0},
            {"name": "beta",  "type": "int",   "default": 0,   "min": -100, "max": 100}
        ]
    },
    "Invert": {
        "function": invert_image,
        "params": []
    },
    "Erode": {
        "function": erode,
        "params": [
            {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 31},
            {"name": "iterations",  "type": "int", "default": 1, "min": 1, "max": 10}
        ]
    },
    "Dilate": {
        "function": dilate,
        "params": [
            {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 31},
            {"name": "iterations",  "type": "int", "default": 1, "min": 1, "max": 10}
        ]
    },
    "Open (Morph)": {
        "function": open_morph,
        "params": [
            {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 31},
        ]
    },
    "Close (Morph)": {
        "function": close_morph,
        "params": [
            {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 31},
        ]
    },
    "Gradient (Morph)": {
        "function": gradient_morph,
        "params": [
            {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 31},
        ]
    },
    "Top-hat (Morph)": {
        "function": tophat_morph,
        "params": [
            {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 31},
        ]
    },
    "Black-hat (Morph)": {
        "function": blackhat_morph,
        "params": [
            {"name": "kernel_size", "type": "int", "default": 3, "min": 1, "max": 31},
        ]
    },
    "Binary Threshold": {
        "function": threshold_binary,
        "params": [
            {"name": "thresh_val", "type": "int", "default": 127, "min": 0,   "max": 255},
            {"name": "max_val",    "type": "int", "default": 255, "min": 1,   "max": 255},
            {"name": "invert",     "type": "bool", "default": False},
        ]
    },
    "Otsu Threshold": {
        "function": threshold_otsu,
        "params": []
    },
    "Adaptive Threshold": {
        "function": adaptive_threshold,
        "params": [
            {"name": "block_size", "type": "int", "default": 11,  "min": 3,  "max": 101},
            {"name": "C",          "type": "int", "default": 2,   "min": -10, "max": 10},
            {"name": "method",     "type": "list", "values": ["mean", "gaussian"], "default": "mean"}
        ]
    },
    "Hist Equalization": {
        "function": histogram_equalization,
        "params": []
    },
    "CLAHE": {
        "function": clahe,
        "params": [
            {"name": "clip_limit", "type": "float", "default": 2.0, "min": 0.1, "max": 10.0},
            {"name": "tile_size",  "type": "int",   "default": 8,    "min": 1,   "max": 64}
        ]
    },
    "Rotate": {
        "function": rotate,
        "params": [
            {"name": "angle", "type": "float", "default": 90.0, "min": -360.0, "max": 360.0}
        ]
    },
    "Flip": {
        "function": flip,
        "params": [
            {"name": "flip_code", "type": "list", "values": ["Horizontal (1)", "Vertical (0)", "Both (-1)"], "default": "Horizontal (1)"}
        ]
    },
    "Resize": {
        "function": resize,
        "params": [
            {"name": "width", "type": "int_none", "default": None, "min": 1, "max": 9999},
            {"name": "height", "type": "int_none", "default": None, "min": 1, "max": 9999}
        ]
    },
    "Crop": {
        "function": crop,
        "params": [
            {"name": "x", "type": "int", "default": 0, "min": 0, "max": 9999},
            {"name": "y", "type": "int", "default": 0, "min": 0, "max": 9999},
            {"name": "w", "type": "int", "default": 100, "min": 1, "max": 9999},
            {"name": "h", "type": "int", "default": 100, "min": 1, "max": 9999},
        ]
    },
    # ... You could keep adding more operations ...
}
