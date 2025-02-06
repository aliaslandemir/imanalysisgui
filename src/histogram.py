import cv2
import numpy as np
from matplotlib.figure import Figure

def compute_histogram(image):
    """
    Computes histogram data for the RGB channels.
    Returns a list (or array) of hist values for each color channel.
    Each channel array has shape (256,).
    """
    # image is assumed to be in RGB
    hists = []
    for i in range(3):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        hists.append(hist)
    return hists

def create_histogram_figure(image):
    """
    Creates a matplotlib Figure for the histogram of the RGB image.
    Returns the figure object (you can embed in PyQt).
    """
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("Histogram")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")

    if image is None:
        ax.text(0.5, 0.5, 'No Image Loaded',
                ha='center', va='center', fontsize=12)
    else:
        for i, color in enumerate(('r', 'g', 'b')):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            ax.plot(hist, color=color)
        ax.set_xlim([0, 256])
        ax.grid(True)
    fig.tight_layout()
    return fig
