import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QToolBar, QFileDialog, QVBoxLayout, \
    QHBoxLayout, QSizePolicy, QAction
from PyQt5.QtCore import QSize
from FilePC import FilePC
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.original_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar_original_plot = NavigationToolbar2QT(self.original_plot, self)

        self.setWindowTitle("Application")
        self.setMinimumSize(QSize(400, 300))

        toolbar = QToolBar('toolbar')
        self.addToolBar(toolbar)

        self.button_file = QAction('Файл')
        self.button_file.triggered.connect(self.open_file)
        toolbar.addAction(self.button_file)

        self.description = QLabel('')
        self.filters = QLabel('filtersgjghjghjghjghg')

        self.layout_vertical1 = QVBoxLayout()
        self.layout_vertical1.addWidget(self.filters)

        self.layout_vertical2 = QVBoxLayout()
        self.layout_vertical2.addWidget(self.toolbar_original_plot, 1)
        self.layout_vertical2.addWidget(self.original_plot, 8)
        self.layout_vertical2.addWidget(self.description, 1)

        self.layout_horizontal = QHBoxLayout()
        self.layout_horizontal.addLayout(self.layout_vertical1, 1)
        self.layout_horizontal.addLayout(self.layout_vertical2, 9)

        self.main_container = QWidget()
        self.main_container.setLayout(self.layout_horizontal)

    def open_file(self):
        file_name = QFileDialog.getOpenFileName()
        file_pc = FilePC(file_name[0])
        is_successful = file_pc.read()
        if is_successful:
            self.description.setText(str(file_pc))
            self.original_plot.axes.cla()
            self.original_plot.axes.plot(file_pc.samples)
            self.original_plot.draw()
            self.show_interface()

    def show_interface(self):
        self.setCentralWidget(self.main_container)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
