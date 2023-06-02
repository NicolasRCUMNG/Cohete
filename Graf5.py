# Se importan todas las librerías necesarias
import sys
import serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pyqtgraph as pg
import csv

class SerialPlot(QWidget):
    def __init__(self, parent=None):
        super(SerialPlot, self).__init__(parent)

        # Configuración de la ventana principal
        self.setWindowTitle("Datos del cohete")
        self.setGeometry(0, 0, 800, 600)

        # Configuración de los gráficos
        self.graphWidgets = []
        self.graphWidgets.append(self.createGraphWidget(50, 50, 'Aceleración', ['AcX', 'AcY', 'AcZ']))
        self.graphWidgets.append(self.createGraphWidget(50, 300, 'Giroscopio', ['GyX', 'GyY', 'GyZ']))
        self.graphWidgets.append(self.createGraphWidget(50, 550, 'Altura', ['Altura']))

        # Configuración del puerto serial
        self.ser = serial.Serial('COM13', 9600)
        self.ser.flush()

        # Variables para almacenar los datos
        num_points = 100  # Número de puntos a mostrar en la gráfica
        self.x_data = np.zeros(num_points)  # Tiempo
        self.y_data = [[] for _ in range(len(self.graphWidgets))]

        # Crear las líneas para cada valor a graficar
        self.curves = [[] for _ in range(len(self.graphWidgets))]
        for i, graphWidget in enumerate(self.graphWidgets):
            for j, label in enumerate(graphWidget['labels']):
                curve = graphWidget['widget'].plot(self.x_data, self.y_data[i][j], pen=pg.mkPen(color=j, width=1), name=label)
                self.curves[i].append(curve)

        layout = QHBoxLayout()
        for graphWidget in self.graphWidgets:
            layout.addWidget(graphWidget['widget'])
        self.setLayout(layout)
        self.showFullScreen()  # Utilizar la pantalla completa

        # Configuración del temporizador para actualizar los datos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10)

        # Configuración del archivo CSV para guardar los datos
        self.csv_filename = 'data.csv'
        self.csv_file = open(self.csv_filename, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Tiempo'] + [label for graphWidget in self.graphWidgets for label in graphWidget['labels']])

    def createGraphWidget(self, x, y, title, labels):
        graphWidget = pg.PlotWidget(self)
        graphWidget.setGeometry(x, y, 600, 200)
        graphWidget.setBackground('w')
        graphWidget.showGrid(x=True, y=True)
        graphWidget.setTitle(title)
        graphWidget.setLabel('left', 'Magnitud')
        graphWidget.setLabel('bottom', 'Muestras')

        return {'widget': graphWidget, 'labels': labels}

    def update_data(self):
        # Leer los datos del puerto serie
        line = self.ser.readline().decode().strip()
        values = line.split(',')

        # Añadir los nuevos valores a los datos
        for i in range(len(self.graphWidgets)):
            for j in range(len(self.graphWidgets[i]['labels'])):
                self.y_data[i][j][:-1] = self.y_data[i][j][1:]
                self.y_data[i][j][-1] = float(values[j])
                self.curves[i][j].setData(self.x_data, self.y_data[i][j])

        # Guardar los datos en el archivo CSV
        data_row = [self.x_data[-1]] + [value for sublist in self.y_data[i] for value in sublist]
        self.csv_writer.writerow(data_row)

        def resizeEvent(self, event):
        # Actualizar el tamaño de los gráficos al cambiar el tamaño de la ventana
         for graphWidget in self.graphWidgets: 
            graphWidget['widget'].setGeometry(50, graphWidget['widget'].y(), self.width() - 100, graphWidget['widget'].height())

        def closeEvent(self, event):
        # Cerrar el archivo CSV al cerrar la aplicación
         self.csv_file.close()

        if __name__ == '__main__':
         app = QApplication(sys.argv)
        ex = SerialPlot()
        ex.show()
        sys.exit(app.exec_())
