#include <SPI.h>  // incluye libreria SPI para comunicacion con el modulo
#include <RH_NRF24.h> // incluye la seccion NRF24 de la libreria RadioHead
#include <Wire.h>    // incluye libreria de bus I2C
#include <Adafruit_Sensor.h>  // incluye librerias para sensor BMP280
#include <Adafruit_BMP280.h>
RH_NRF24 nrf24;   // crea objeto con valores por defecto para bus SPI
      // y pin digital numero 8 para CE
Adafruit_BMP280 bmp;
float TEMPERATURA;    // variable para almacenar valor de temperatura
float PRESION, P0;    // variables para almacenar valor de presion atmosferica
        // y presion actual como referencia para altitud
float PRESION_1; 
float ALTURA,ALTURA1;


String str_presion; // string para almacenar valor de PRESION
String str_temperatura; // string para almacenar valor de temperatura
String str_altura;//string para almacenar valor de altura
String str_datos; // string para almacenar valores separados por coma

void setup() 
{
  Serial.begin(9600);   // inicializa monitor serie a 9600 bps
  if (!nrf24.init())    // si falla inicializacion de modulo muestra texto
    Serial.println("fallo de inicializacion");
  if (!nrf24.setChannel(100)) // si falla establecer canal muestra texto
    Serial.println("fallo en establecer canal");
  if (!nrf24.setRF(RH_NRF24::DataRate250kbps, RH_NRF24::TransmitPowerm12dBm)) // si falla opciones 
    Serial.println("fallo en opciones RF");           // RF muestra texto

    
    Serial.println("Iniciando:");      // texto de inicio
  if ( !bmp.begin() ) {       // si falla la comunicacion con el sensor mostrar
    Serial.println("BMP280 no encontrado !"); // texto y detener flujo del programa
    while (1);          // mediante bucle infinito
  }
  P0 = bmp.readPressure()/100;      // almacena en P0 el valor actual de presion
}

void loop()
{
    TEMPERATURA = bmp.readTemperature();  // obtiene y almacena temperatura
    PRESION = bmp.readPressure()/100;   // obtiene y almacena humedad
    PRESION_1=PRESION/100;
    ALTURA=bmp.readAltitude(P0);
//   Serial.println(TEMPERATURA);
//    Serial.println(PRESION);
    
    if(ALTURA<0)
    {
      ALTURA=ALTURA*-1;
      }
//    Serial.print(ALTURA);
    str_temperatura = String(TEMPERATURA);  // convierte a string valor entero de temperatura
    str_presion = String(PRESION_1);    // convierte a string valor entero de humedad
    str_altura = String(ALTURA);
    
    str_datos = str_temperatura + "," + str_presion + "," + str_altura;  // concatena valores separados mediante una coma
    Serial.println(str_datos);  
    Serial.println(str_datos);
    static char *datos = str_datos.c_str();   // convierte a string en formato de lenguaje C
    
    nrf24.send((uint8_t *)datos, strlen(datos));  // envia datos
    nrf24.waitPacketSent();       // espera hasta realizado el envio
    delay(100);          // demora de 1 segundo entre envios
}
