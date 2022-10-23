import matplotlib
matplotlib.use('Qt5Agg')

import scipy.signal
import scipy.fft
import numpy as np
import pycwt

from filters import filter_wiener, decompose_fourier
from filters_windows import WindowFourier

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QToolBar, QFileDialog, QVBoxLayout, \
    QHBoxLayout, QAction, QSpinBox
from PyQt5.QtCore import QSize
from FilePC import FilePC
from MplCanvas import MplCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.file_pc = None
        self.window_filter = None

        self.setWindowTitle("Application")
        self.setMinimumSize(QSize(400, 300))

        toolbar = QToolBar('toolbar')
        self.addToolBar(toolbar)

        self.button_file = QAction('Файл')
        self.button_file.triggered.connect(self.open_file)
        toolbar.addAction(self.button_file)

        self.init_filters_container()
        self.init_plots_container()

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
            self.file_pc = file_pc
            self.description.setText(str(self.file_pc))
            self.original_plot.axes.cla()
            self.original_plot.axes.plot(self.file_pc.samples)
            self.original_plot.draw()
            self.filtered_plot.axes.cla()
            self.filtered_plot.draw()
            self.show_interface()

    def init_filters_container(self):
        self.container_fourier = QVBoxLayout()
        self.button_decompose_fourier = QPushButton('Преобразование Фурье')
        self.button_decompose_fourier.clicked.connect(self.slot_decompose_fourier)
        self.container_fourier.addWidget(self.button_decompose_fourier)
        #self.container_fourier.addWidget(self.decompose_fourier_plot, 8)
        #self.container_fourier.addWidget(self.button_filter_fourier, 1)

        self.container_wavelet = QVBoxLayout()
        self.button_filter_wavelet = QPushButton('Вейвлет фильтр')
        self.button_filter_wavelet.clicked.connect(self.slot_filter_wavelet)
        self.container_wavelet.addWidget(self.button_filter_wavelet)

        self.container_wiener = QVBoxLayout()
        self.button_filter_wiener = QPushButton('Винеровский фильтр')
        self.button_filter_wiener.clicked.connect(self.slot_filter_wiener)
        self.label_window_wiener = QLabel('Ширина окна:')
        self.window_wiener = QSpinBox()
        self.window_wiener.setMaximum(10000)
        self.window_wiener.setMinimum(3)
        self.window_wiener.setValue(1000)
        self.container_wiener.addWidget(self.button_filter_wiener)
        self.container_wiener.addWidget(self.label_window_wiener)
        self.container_wiener.addWidget(self.window_wiener)

        self.description = QLabel('')

        self.layout_vertical1 = QVBoxLayout()
        self.layout_vertical1.addLayout(self.container_fourier, 1)
        self.layout_vertical1.addLayout(self.container_wavelet, 1)
        self.layout_vertical1.addLayout(self.container_wiener, 1)
        self.layout_vertical1.addWidget(self.description, 1)

    def init_plots_container(self):
        self.original_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar_original_plot = NavigationToolbar2QT(self.original_plot, self)

        self.filtered_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar_filtered_plot = NavigationToolbar2QT(self.filtered_plot, self)

        self.layout_vertical2 = QVBoxLayout()
        self.layout_vertical2.addWidget(self.toolbar_original_plot, 1)
        self.layout_vertical2.addWidget(self.original_plot, 4)
        self.layout_vertical2.addWidget(self.toolbar_filtered_plot, 1)
        self.layout_vertical2.addWidget(self.filtered_plot, 4)

    def slot_decompose_fourier(self):
        original_data = np.array(self.file_pc.samples)
        amplitudes, frequencies = decompose_fourier(original_data, 100)
        self.window_filter = WindowFourier()
        self.window_filter.build_decomposed_plot(amplitudes, frequencies, self.file_pc.sample_rate)
        self.window_filter.filter_applied.connect(self.slot_filter_fourier)
        self.window_filter.show()

    def slot_filter_fourier(self, filtered_data):
        self.filtered_plot.axes.cla()
        self.filtered_plot.axes.plot(filtered_data)
        self.filtered_plot.draw()

    def slot_filter_wavelet(self):
        original_data = np.array(self.file_pc.samples)
        wave, scales, freqs, coi, fft, fftfreqs = pycwt.cwt(original_data, dt=180, dj=0.1)  # J=19)
        pc = 20000
        restored_icwt = pycwt.icwt(wave[29:76], scales[29:76], dj=0.1, dt=180 * pc)  # Last element not included
        self.filtered_plot.axes.cla()
        self.filtered_plot.axes.plot(restored_icwt)
        self.filtered_plot.draw()

    def slot_filter_wiener(self):
        original_data = np.array(self.file_pc.samples)
        filtered_data = filter_wiener(original_data, self.window_wiener.value())
        self.filtered_plot.axes.cla()
        self.filtered_plot.axes.plot(filtered_data)
        self.filtered_plot.draw()

    def show_interface(self):
        self.setCentralWidget(self.main_container)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
