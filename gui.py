import sys
import numpy as np
import cv2

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDockWidget, QFileDialog,
    QMessageBox, QVBoxLayout, QLabel, QComboBox, QPushButton, QToolBar,
    QStatusBar, QScrollArea, QFormLayout, QSpinBox, QDoubleSpinBox,
    QCheckBox, QLineEdit
)
from PyQt6.QtGui import (
    QAction, QPainter, QPen, QColor, QPixmap, QImage, QTransform
)
from PyQt6.QtCore import Qt, QRect, QPoint, QRunnable, QThreadPool, pyqtSignal, QObject

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

rcParams.update({'font.size': 8, 'axes.grid': True})

# Import your custom modules (assumed to exist in src/)
from src.image_ops import read_image, write_image
from src.utils import FILTERS_MAP  # This dictionary maps operation names -> {function, params}

# ============================
# Async Worker
# ============================
class WorkerSignals(QObject):
    finished = pyqtSignal(np.ndarray)
    error = pyqtSignal(str)

class ProcessingTask(QRunnable):
    def __init__(self, func, image, kwargs=None):
        super().__init__()
        self.func = func
        self.image = image
        self.kwargs = kwargs if kwargs else {}
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.func(self.image, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))

# ============================
# Image Canvas
# ============================
class ImageCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_image = None
        self.display_image = None
        self.zoom_factor = 1.0
        self.dragging = False
        self.last_pos = QPoint(0, 0)
        self.roi = QRect(0, 0, 0, 0)
        self.pixmap = None
        self.pan_start = QPoint(0, 0)
        self.offset = QPoint(0, 0)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def load_image(self, path):
        try:
            img = read_image(path)
            self.original_image = img.copy()
            self.display_image = img.copy()
            self.update_display()
            return True
        except Exception as e:
            QMessageBox.critical(self.parent(), "Error", f"Failed to load image:\n{str(e)}")
            return False

    def set_image(self, image):
        if image is None:
            return
        self.original_image = image.copy()
        self.display_image = image.copy()
        self.update_display()

    def update_display(self):
        if self.display_image is None:
            return
        h, w, _ = self.display_image.shape
        qimg = QImage(self.display_image.data, w, h, 3 * w, QImage.Format.Format_RGB888).rgbSwapped()
        self.pixmap = QPixmap.fromImage(qimg)
        self.update()

    def paintEvent(self, event):
        if not self.pixmap:
            return
        painter = QPainter(self)
        transform = QTransform().scale(self.zoom_factor, self.zoom_factor)
        scaled_pix = self.pixmap.transformed(transform)
        painter.drawPixmap(self.offset, scaled_pix)

        # Optionally draw ROI or something else
        if not self.roi.isNull():
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.DashLine))
            painter.drawRect(self.roi)

    def wheelEvent(self, event):
        factor = 1.2 if event.angleDelta().y() > 0 else 1 / 1.2
        self.zoom_factor = max(0.1, min(10.0, self.zoom_factor * factor))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_pos = event.pos()
            self.pan_start = event.pos()
            self.roi.setTopLeft(event.pos())
            self.roi.setBottomRight(event.pos())

    def mouseMoveEvent(self, event):
        if self.dragging:
            # For demonstration, just update ROI
            self.roi.setBottomRight(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = False

# ============================
# Histogram Widget
# ============================
class HistogramWidget(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 3), dpi=100)
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.ax.set_title("Histogram")
        self.ax.set_xlabel("Pixel Value")
        self.ax.set_ylabel("Frequency")
        fig.tight_layout()

    def update_histogram(self, image):
        self.ax.clear()
        if image is None:
            self.ax.text(0.5, 0.5, "No Image Loaded",
                         ha="center", va="center", fontsize=12)
        else:
            for i, color in enumerate(['r', 'g', 'b']):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                self.ax.plot(hist, color=color)
            self.ax.set_xlim([0, 256])
            self.ax.grid(True)
        self.draw()

# ============================
# Dynamic (Operation) Parameters Widget
# ============================
class OperationParametersWidget(QWidget):
    """
    Dynamically creates parameter controls based on the operation's
    definition in FILTERS_MAP.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QFormLayout(self)
        self.param_controls = {}

    def build_ui_for_operation(self, op_name: str):
        # Clear previous controls
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.param_controls.clear()

        if op_name not in FILTERS_MAP:
            return

        param_defs = FILTERS_MAP[op_name]["params"]
        for pdef in param_defs:
            name = pdef["name"]
            ptype = pdef["type"]
            default = pdef["default"]

            if ptype == "int":
                spin = QSpinBox()
                spin.setMinimum(pdef.get("min", -9999))
                spin.setMaximum(pdef.get("max", 9999))
                spin.setValue(default)
                self.layout.addRow(f"{name}:", spin)
                self.param_controls[name] = spin
            elif ptype == "float":
                dspin = QDoubleSpinBox()
                dspin.setMinimum(pdef.get("min", -9999.0))
                dspin.setMaximum(pdef.get("max", 9999.0))
                dspin.setValue(default)
                dspin.setDecimals(2)
                self.layout.addRow(f"{name}:", dspin)
                self.param_controls[name] = dspin
            elif ptype == "bool":
                cbox = QCheckBox()
                cbox.setChecked(bool(default))
                self.layout.addRow(f"{name}:", cbox)
                self.param_controls[name] = cbox
            elif ptype == "list":
                combo = QComboBox()
                values = pdef["values"]
                for v in values:
                    combo.addItem(str(v))
                if default in values:
                    combo.setCurrentIndex(values.index(default))
                self.layout.addRow(f"{name}:", combo)
                self.param_controls[name] = combo
            elif ptype == "int_none":
                line = QLineEdit()
                line.setText("None" if default is None else str(default))
                self.layout.addRow(f"{name}:", line)
                self.param_controls[name] = line
            else:
                # fallback: a string param
                line = QLineEdit(str(default))
                self.layout.addRow(f"{name}:", line)
                self.param_controls[name] = line

    def get_parameters(self, op_name: str):
        params = {}
        if op_name not in FILTERS_MAP:
            return params

        param_defs = FILTERS_MAP[op_name]["params"]
        for pdef in param_defs:
            name = pdef["name"]
            ptype = pdef["type"]
            widget = self.param_controls.get(name)
            if widget is None:
                continue

            if ptype == "int":
                params[name] = widget.value()
            elif ptype == "float":
                params[name] = widget.value()
            elif ptype == "bool":
                params[name] = widget.isChecked()
            elif ptype == "list":
                textval = widget.currentText()
                # Example parsing for "Flip"
                if "Horizontal" in textval:
                    params[name] = 1
                elif "Vertical" in textval:
                    params[name] = 0
                elif "Both" in textval:
                    params[name] = -1
                else:
                    params[name] = textval
            elif ptype == "int_none":
                txt = widget.text().strip()
                if txt.lower() == "none":
                    params[name] = None
                else:
                    params[name] = int(txt)
            else:
                params[name] = widget.text()

        return params

# ============================
# Main Window with Multiple Operation Docks
# ============================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Analysis GUI")
        self.setGeometry(100, 100, 1600, 1000)

        # Image / History
        self.image_history = []
        self.current_index = -1
        self.current_image = None

        # Threadpool for async ops
        self.threadpool = QThreadPool()

        # Central Canvas
        self.canvas = ImageCanvas()
        self.setCentralWidget(self.canvas)

        # Histogram Dock
        self.hist_dock = QDockWidget("Histogram", self)
        self.histogram_widget = HistogramWidget()
        self.hist_dock.setWidget(self.histogram_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.hist_dock)

        # We define categories of operations as sets of filter names
        # that appear in FILTERS_MAP
        self.filters_ops = [
            "Gaussian Blur", "Median Filter", "Bilateral Filter",
            "Canny Edge", "Sobel Edge", "Laplacian Edge", 
            "Unsharp Mask", "Gamma Correction", 
            "Brightness/Contrast", "Invert"
        ]

        self.geometry_ops = [
            "Rotate", "Flip", "Resize", "Crop"
        ]

        self.image_ops_ops = [
            "Binary Threshold", "Otsu Threshold", "Adaptive Threshold",
            "Hist Equalization", "CLAHE"
        ]

        self.morph_ops = [
            "Erode", "Dilate", "Open (Morph)", "Close (Morph)",
            "Gradient (Morph)", "Top-hat (Morph)", "Black-hat (Morph)"
        ]

        # Create a dock for each category
        self.filters_dock = self.create_operation_dock("Filters", self.filters_ops)
        self.geometry_dock = self.create_operation_dock("Geometry", self.geometry_ops)
        self.image_ops_dock = self.create_operation_dock("Image Ops", self.image_ops_ops)
        self.morph_dock = self.create_operation_dock("Morphological", self.morph_ops)

        # Place the docks around
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.filters_dock)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.geometry_dock)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.image_ops_dock)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.morph_dock)

        # Split the left side so "Filters" and "Morphological" can be viewed together
        self.splitDockWidget(self.filters_dock, self.morph_dock, Qt.Orientation.Vertical)

        # Menu / Toolbar
        self.create_menu_toolbar()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_operation_dock(self, title: str, operations: list) -> QDockWidget:
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel("Select Operation:")
        layout.addWidget(label)

        combo = QComboBox()
        combo.addItems(operations)
        layout.addWidget(combo)

        params_widget = OperationParametersWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(params_widget)
        layout.addWidget(scroll)

        apply_btn = QPushButton("Apply")
        layout.addWidget(apply_btn)

        widget.setLayout(layout)
        dock.setWidget(widget)

        # Connect
        combo.currentTextChanged.connect(lambda op: params_widget.build_ui_for_operation(op))
        if operations:
            params_widget.build_ui_for_operation(operations[0])

        apply_btn.clicked.connect(lambda: self.apply_operation(combo.currentText(), params_widget))

        return dock

    def apply_operation(self, op_name: str, params_widget: OperationParametersWidget):
        if self.current_image is None:
            QMessageBox.warning(self, "No Image", "Please load an image first.")
            return
        if op_name not in FILTERS_MAP:
            QMessageBox.warning(self, "Operation Error", f"'{op_name}' not found in FILTERS_MAP.")
            return

        func = FILTERS_MAP[op_name]["function"]
        kwargs = params_widget.get_parameters(op_name)
        task = ProcessingTask(func, self.current_image.copy(), kwargs)
        task.signals.finished.connect(self.on_operation_done)
        task.signals.error.connect(self.on_operation_error)
        self.threadpool.start(task)
        self.status_bar.showMessage(f"Applying {op_name}...", 3000)

    def on_operation_done(self, result):
        self.set_image_and_update(result)
        self.status_bar.showMessage("Operation complete", 2000)

    def on_operation_error(self, message):
        QMessageBox.critical(self, "Operation Error", message)

    def create_menu_toolbar(self):
        open_act = QAction("Open", self)
        open_act.triggered.connect(self.open_image)

        save_act = QAction("Save", self)
        save_act.triggered.connect(self.save_image)

        self.undo_act = QAction("Undo", self)
        self.undo_act.triggered.connect(self.undo)
        self.undo_act.setEnabled(False)

        self.redo_act = QAction("Redo", self)
        self.redo_act.triggered.connect(self.redo)
        self.redo_act.setEnabled(False)

        toolbar = QToolBar("Main Toolbar")
        # IMPORTANT: Use ToolBarArea.* instead of DockWidgetArea.*
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        toolbar.addAction(open_act)
        toolbar.addAction(save_act)
        toolbar.addAction(self.undo_act)
        toolbar.addAction(self.redo_act)

    # -----------------------
    # Image / History
    # -----------------------
    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.tif *.tiff)"
        )
        if path:
            if self.canvas.load_image(path):
                self.current_image = self.canvas.display_image.copy()
                self.update_history()
                self.histogram_widget.update_histogram(self.current_image)
                self.status_bar.showMessage(f"Loaded: {path}", 5000)

    def save_image(self):
        if self.current_image is None:
            QMessageBox.warning(self, "No Image", "Please load or process an image first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Images (*.png *.jpg *.tif *.tiff)"
        )
        if path:
            write_image(path, self.current_image)
            self.status_bar.showMessage(f"Saved: {path}", 5000)

    def set_image_and_update(self, image):
        self.current_image = image.copy()
        self.canvas.set_image(self.current_image)
        self.histogram_widget.update_histogram(self.current_image)
        self.update_history()

    def update_history(self):
        if self.current_image is None:
            return
        self.image_history = self.image_history[:self.current_index + 1]
        self.image_history.append(self.current_image.copy())
        self.current_index += 1
        self.undo_act.setEnabled(self.current_index > 0)
        self.redo_act.setEnabled(False)

    def undo(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.current_image = self.image_history[self.current_index].copy()
            self.canvas.set_image(self.current_image)
            self.histogram_widget.update_histogram(self.current_image)
            self.undo_act.setEnabled(self.current_index > 0)
            self.redo_act.setEnabled(True)

    def redo(self):
        if self.current_index < len(self.image_history) - 1:
            self.current_index += 1
            self.current_image = self.image_history[self.current_index].copy()
            self.canvas.set_image(self.current_image)
            self.histogram_widget.update_histogram(self.current_image)
            self.undo_act.setEnabled(True)
            self.redo_act.setEnabled(self.current_index < len(self.image_history) - 1)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
