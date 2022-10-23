from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDoubleSpinBox, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from MplCanvas import MplCanvas
from filters import filter_fourier
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class WindowFourier(QWidget):
    rate = None
    amplitudes = None
    amplitudes_to_show = None
    frequencies = None
    filter_applied = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.decompose_fourier_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar_decompose_plot = NavigationToolbar2QT(self.decompose_fourier_plot, self)
        self.button_filter_fourier = QPushButton('Наложить фильтр')
        self.button_filter_fourier.clicked.connect(self.slot_filter_fourier)

        self.spinbox_low_pass = QDoubleSpinBox()
        self.spinbox_low_pass.setMinimum(0)
        self.spinbox_low_pass.setMaximum(49)
        self.spinbox_low_pass.setValue(0)
        self.spinbox_low_pass.valueChanged.connect(self.slot_spinbox_changed)
        self.spinbox_high_pass = QDoubleSpinBox()
        self.spinbox_high_pass.setMinimum(1)
        self.spinbox_high_pass.setMaximum(50)
        self.spinbox_high_pass.setValue(50)
        self.spinbox_high_pass.valueChanged.connect(self.slot_spinbox_changed)
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(QLabel("Нижний порог (Гц):"))
        settings_layout.addWidget(self.spinbox_low_pass, 2)
        settings_layout.addStretch(1)
        settings_layout.addWidget(QLabel("Верхний порог (Гц):"))
        settings_layout.addWidget(self.spinbox_high_pass, 2)

        layout.addWidget(self.toolbar_decompose_plot, 1)
        layout.addWidget(self.decompose_fourier_plot, 6)
        layout.addLayout(settings_layout, 1)
        layout.addStretch(1)
        layout.addWidget(self.button_filter_fourier, 1)

        self.setLayout(layout)

    def slot_filter_fourier(self):
        filtered_data = filter_fourier(self.amplitudes,
                                       self.frequencies,
                                       self.rate,
                                       self.spinbox_low_pass.value(),
                                       self.spinbox_high_pass.value()
                                       )
        filtered_data = filtered_data.tolist()
        self.filter_applied.emit(filtered_data)
        self.close()

    def build_decomposed_plot(self, amplitudes, frequencies, rate):
        self.rate = rate
        self.amplitudes = amplitudes
        self.amplitudes_to_show = amplitudes
        self.frequencies = frequencies
        self.update_decomposed_plot()

    def slot_spinbox_changed(self):
        points_per_freq = len(self.frequencies) / (self.rate / 2)
        self.amplitudes_to_show = self.amplitudes.copy()
        self.amplitudes_to_show[: int(points_per_freq * self.spinbox_low_pass.value()/2)] = 0
        self.amplitudes_to_show[-int(points_per_freq * self.spinbox_low_pass.value()/2) + int(len(self.amplitudes_to_show)):] = 0
        self.amplitudes_to_show[int(points_per_freq * self.spinbox_high_pass.value()/2): int(len(self.amplitudes_to_show)/2)] = 0
        self.amplitudes_to_show[int(len(self.amplitudes_to_show)/2): -int(points_per_freq * self.spinbox_high_pass.value()/2) + int(len(self.amplitudes_to_show))] = 0
        self.update_decomposed_plot()

    def update_decomposed_plot(self):
        self.decompose_fourier_plot.axes.cla()
        self.decompose_fourier_plot.axes.plot(self.frequencies, np.abs(self.amplitudes_to_show))
        self.decompose_fourier_plot.fig.canvas.draw_idle()

