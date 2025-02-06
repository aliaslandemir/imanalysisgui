# imanalysisgui

**Advanced Image Analysis GUI**

imanalysisgui is an advanced, ImageJ‑style GUI built with PyQt6 and OpenCV for common image analysis tasks. The project is highly modular—the processing functions (filters, geometry, image operations, morphological operations, etc.) are organized in the `src` folder. The GUI features a central image canvas, a histogram display, and multiple docks that let you access different categories of image processing operations all at once.

## Table of Contents

- [Features](#features)
- [Screenshot](#screenshot)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Central Canvas:** Load and display images.
- **Dynamic Docks:** Separate docks for:
  - **Filters:** e.g., Gaussian Blur, Median Filter, Canny Edge.
  - **Geometry:** e.g., Rotate, Flip, Resize, Crop.
  - **Image Ops:** e.g., Thresholding, Histogram Equalization, CLAHE.
  - **Morphological Operations:** e.g., Erode, Dilate, Open, Close.
- **Dynamic Parameters:** UI controls that update based on the selected operation.
- **Asynchronous Processing:** Uses a thread pool (QRunnable) to ensure the GUI remains responsive.
- **Undo/Redo History:** Step backwards and forwards through applied operations.
- **Histogram Display:** Visualize the image histogram for RGB channels.

## Screenshot

Below is a screenshot of the GUI.

![Screenshot](docs/screenshot.png)

## Project Structure


imanalysisgui/
├── docs/
│   └── screenshot.png       # Screenshot of the GUI
├── gui.py                   # Main GUI application
├── src/
│   ├── __init__.py          # Package initializer
│   ├── image_ops.py         # Basic image operations (read, write, split, etc.)
│   ├── filters.py           # Filtering functions (Gaussian, Median, etc.)
│   ├── geometry.py          # Geometric transformations (rotate, flip, resize, crop)
│   ├── morphological.py     # Morphological operations (erode, dilate, etc.)
│   └── utils.py             # Utility functions and FILTERS_MAP
├── .gitignore               # Git ignore file
├── README.md                # This file
└── requirements.txt         # Dependencies list
Installation
Clone the repository:

bash
Copy
git clone https://github.com/<your-username>/imanalysisgui.git
cd imanalysisgui
Create a virtual environment (optional but recommended):

bash
Copy
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install dependencies:

bash
Copy
pip install -r requirements.txt
Usage
Run the GUI by executing:

bash
Copy
python gui.py
Once launched, the GUI displays:

A central canvas for your image.
A histogram panel (on the right) showing RGB channel histograms.
Multiple docks (Filters, Geometry, Image Ops, Morphological) on different sides of the window. Use these to select operations, adjust their parameters, and apply them to your image.
Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests. If you add new image processing functions, please update the FILTERS_MAP in src/utils.py so the new operations appear in the GUI.

License
This project is licensed under the MIT License. See the LICENSE file for details.
