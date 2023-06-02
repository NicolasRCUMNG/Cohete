##VISUAL STUDIO CODE##
import serial
import time
import numpy as np
import matplotlib.pyplot as plt

# Establecer la comunicación serial con Arduino
arduino = serial.Serial('COM13', 9600)

# Configurar la ventana de gráficos
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
plt.subplots_adjust(hspace=0.5)

# Inicializar las variables para almacenar los datos
x_acc = []
y_acc = []
z_acc = []
x_gyro = []
y_gyro = []
z_gyro = []

# Función para actualizar los datos y graficarlos en tiempo real
def update():
    # Leer los datos desde Arduino
    data = arduino.readline().decode('utf-8').strip().split(',')
    # Convertir los datos a valores numéricos
    acc_x = float(data[0])
    acc_y = float(data[1])
    acc_z = float(data[2])
    gyro_x = float(data[3])
    gyro_y = float(data[4])
    gyro_z = float(data[5])
    # Almacenar los datos
    x_acc.append(acc_x)
    y_acc.append(acc_y)
    z_acc.append(acc_z)
    x_gyro.append(gyro_x)
    y_gyro.append(gyro_y)
    z_gyro.append(gyro_z)
    # Actualizar las gráficas
    ax1.clear()
    ax1.plot(x_acc, label='X')
    ax1.plot(y_acc, label='Y')
    ax1.plot(z_acc, label='Z')
    ax1.set_title('Acelerómetro')
    ax1.set_ylabel('Aceleración (g)')
    ax1.legend()
    ax2.clear()
    ax2.plot(x_gyro, label='X')
    ax2.plot(y_gyro, label='Y')
    ax2.plot(z_gyro, label='Z')
    ax2.set_title('Giroscopio')
    ax2.set_ylabel('Velocidad angular (°/s)')
    ax2.legend()
    ax3.clear()
    ax3.plot(x_acc[-100:], label='X Acc')
    ax3.plot(y_acc[-100:], label='Y Acc')
    ax3.plot(z_acc[-100:], label='Z Acc')
    ax3.plot(x_gyro[-100:], label='X Gyro')
    ax3.plot(y_gyro[-100:], label='Y Gyro')
    ax3.plot(z_gyro[-100:], label='Z Gyro')
    ax3.set_title('Últimos 100 datos')
    ax3.set_xlabel('Muestras')
    ax3.set_ylabel('Valores')
    ax3.legend()

# Bucle principal
while True:
    update()
    plt.pause(0.001)