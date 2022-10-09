import matplotlib
matplotlib.use('Qt5Agg')

import scipy.signal
import scipy.fft
import numpy as np
import pycwt

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

        self.filtered_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar_filtered_plot = NavigationToolbar2QT(self.filtered_plot, self)

        self.setWindowTitle("Application")
        self.setMinimumSize(QSize(400, 300))

        toolbar = QToolBar('toolbar')
        self.addToolBar(toolbar)

        self.button_file = QAction('Файл')
        self.button_file.triggered.connect(self.open_file)
        toolbar.addAction(self.button_file)

        self.filter_fourier = QPushButton('Фильтр Фурье')
        self.filter_fourier.clicked.connect(self.slot_filter_fourier)
        self.filter_wavelet = QPushButton('Вейвлет фильтр')
        self.filter_wavelet.clicked.connect(self.slot_filter_wavelet)
        self.filter_wiener = QPushButton('Винеровский фильтр')
        self.filter_wiener.clicked.connect(self.slot_filter_wiener)
        self.description = QLabel('')

        self.layout_vertical1 = QVBoxLayout()
        self.layout_vertical1.addWidget(self.filter_fourier, 3)
        self.layout_vertical1.addWidget(self.filter_wavelet, 3)
        self.layout_vertical1.addWidget(self.filter_wiener, 3)
        self.layout_vertical1.addWidget(self.description, 1)

        self.layout_vertical2 = QVBoxLayout()
        self.layout_vertical2.addWidget(self.toolbar_original_plot, 1)
        self.layout_vertical2.addWidget(self.original_plot, 4)
        self.layout_vertical2.addWidget(self.toolbar_filtered_plot, 1)
        self.layout_vertical2.addWidget(self.filtered_plot, 4)

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
            self.filtered_plot.axes.cla()
            self.filtered_plot.draw()
            self.show_interface()

    def slot_filter_fourier(self):
        original_data = np.array(self.original_plot.axes.lines[0].get_data()[1])
        sample_rate = 60001 / 180
        t_f = scipy.fft.fft(original_data)
        t_f_freq = scipy.fft.fftfreq(60001, 1 / sample_rate)

        points_per_freq = len(t_f_freq) / (sample_rate / 2)
        t_f[: int(points_per_freq * 1.4)] = 0
        t_f[int(points_per_freq * 5):] = 0
        filtered_data = scipy.fft.ifft(t_f)
        self.filtered_plot.axes.cla()
        self.filtered_plot.axes.plot(filtered_data)
        self.filtered_plot.draw()

    def slot_filter_wavelet(self):
        original_data = np.array(self.original_plot.axes.lines[0].get_data()[1])
        wave, scales, freqs, coi, fft, fftfreqs = pycwt.cwt(original_data, dt=180, dj=0.1)  # J=19)
        pc = 20000
        restored_icwt = pycwt.icwt(wave[29:76], scales[29:76], dj=0.1, dt=180 * pc)  # Last element not included
        self.filtered_plot.axes.cla()
        self.filtered_plot.axes.plot(restored_icwt)
        self.filtered_plot.draw()

    def slot_filter_wiener(self):
        original_data = np.array(self.original_plot.axes.lines[0].get_data()[1])
        filtered_data = scipy.signal.wiener(original_data, 2500)
        self.filtered_plot.axes.cla()
        self.filtered_plot.axes.plot(filtered_data)
        self.filtered_plot.draw()

    def show_interface(self):
        self.setCentralWidget(self.main_container)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
