# Se importan todas las librerías necesarias
import sys
import serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pyqtgraph as pg

class SerialPlot(QWidget):
    def __init__(self, parent=None):
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal
        self.setWindowTitle("Datos del cohete")
        self.setGeometry(0, 0, 800, 600)

        # Configuración de los gráficos
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(50, 50, 600, 200)
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLabel('left', 'Magnitud')
        self.graphWidget.setLabel('bottom', 'Muestras')

        # Configuración del puerto serial
        self.ser = serial.Serial('COM13', 9600)
        self.ser.flush()

        # Variables para almacenar los datos
        num_points = 100  # Número de puntos a mostrar en la gráfica
        self.x_data = np.zeros(num_points)  # Tiempo
        self.y_data = np.zeros((7, num_points))  # Datos de los sensores

        # Crear las líneas para cada valor a graficar
        self.curves = []
        colors = ['r', 'g', 'b', 'm', 'c', 'y', 'k']
        names = ['AcX', 'AcY', 'AcZ', 'GyX', 'GyY', 'GyZ', 'Altitud']
        for i in range(7):
            curve = self.graphWidget.plot(self.x_data, self.y_data[i], pen=colors[i], name=names[i])
            self.curves.append(curve)

        layout = QHBoxLayout()
        layout.addWidget(self.graphWidget)
        self.setLayout(layout)
        self.showFullScreen()

        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)

    def update_data(self):
        # Leer los datos del puerto serie
        line = self.ser.readline().decode().strip()
        values = line.split(',')

        # Añadir los nuevos valores a los datos de los sensores
        self.y_data[:, :-1] = self.y_data[:, 1:]
        for i in range(7):
            self.y_data[i, -1] = float(values[i])

        # Crear valores para el tiempo
        self.x_data[:-1] = self.x_data[1:]
        self.x_data[-1] = self.x_data[-2] + 1

        # Actualizar las líneas de la gráfica con los nuevos datos
        for i in range(7):
            self.curves[i].setData(self.x_data, self.y_data[i])

    def resizeEvent(self, event):
        # Actualizar el tamaño del gráfico al cambiar el tamaño de la ventana
        self.graphWidget.setGeometry(50, 50, self.width() - 100, self.height() - 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialPlot()
    ex.show()
    sys.exit(app.exec_())
