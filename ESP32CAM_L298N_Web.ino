#include "esp_camera.h"
#include <WiFi.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#define CAMERA_MODEL_AI_THINKER

// ===================
// PINOS
// ===================

#define LED 4

#define RXD2 14
#define TXD2 13

// Motores
int gpLb = 14; // Left Backward
int gpLf = 13; // Left Forward

int gpRb = 33; // Right Backward
int gpRf = 15; // Right Forward

int ENR = 2;
int ENL = 12;

WiFiServer server(100);

void CameraWebServer_init();


// ===================
// INICIAR MOTORES
// ===================

void initMotors()
{
  pinMode(gpLb, OUTPUT);
  pinMode(gpLf, OUTPUT);

  pinMode(gpRb, OUTPUT);
  pinMode(gpRf, OUTPUT);

  pinMode(ENR, OUTPUT);
  pinMode(ENL, OUTPUT);

  pinMode(LED, OUTPUT);

  // PWM ESP32 2.0.17
  ledcSetup(2, 5000, 8);
  ledcSetup(12, 5000, 8);

  ledcAttachPin(ENR, 2);
  ledcAttachPin(ENL, 12);

  ledcWrite(2, 0);
  ledcWrite(12, 0);

  digitalWrite(gpLb, LOW);
  digitalWrite(gpLf, LOW);

  digitalWrite(gpRb, LOW);
  digitalWrite(gpRf, LOW);
}


// ===================
// MOVIMENTOS
// ===================

void forward()
{
  ledcWrite(2, 200);
  ledcWrite(12, 200);

  digitalWrite(gpLb, LOW);
  digitalWrite(gpLf, HIGH);

  digitalWrite(gpRb, LOW);
  digitalWrite(gpRf, HIGH);

  Serial.println("Forward");
}

void back()
{
  ledcWrite(2, 200);
  ledcWrite(12, 200);

  digitalWrite(gpLb, HIGH);
  digitalWrite(gpLf, LOW);

  digitalWrite(gpRb, HIGH);
  digitalWrite(gpRf, LOW);

  Serial.println("Back");
}

void left()
{
  ledcWrite(2, 200);
  ledcWrite(12, 200);

  digitalWrite(gpLb, HIGH);
  digitalWrite(gpLf, LOW);

  digitalWrite(gpRb, LOW);
  digitalWrite(gpRf, HIGH);

  Serial.println("Left");
}

void right()
{
  ledcWrite(2, 200);
  ledcWrite(12, 200);

  digitalWrite(gpLb, LOW);
  digitalWrite(gpLf, HIGH);

  digitalWrite(gpRb, HIGH);
  digitalWrite(gpRf, LOW);

  Serial.println("Right");
}

void stopCar()
{
  ledcWrite(2, 0);
  ledcWrite(12, 0);

  digitalWrite(gpLb, LOW);
  digitalWrite(gpLf, LOW);

  digitalWrite(gpRb, LOW);
  digitalWrite(gpRf, LOW);

  Serial.println("Stop");
}


// ===================
// SETUP
// ===================

void setup()
{
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  Serial.begin(115200);

  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);

  Serial.setDebugOutput(true);

  Serial.println();
  Serial.println("ESP32-CAM INICIADA");

  // Inicializa câmera/webserver
  CameraWebServer_init();

  // Inicializa motores
  initMotors();

  // PWM LED
  ledcSetup(7, 5000, 8);
  ledcAttachPin(LED, 7);

  // Pisca LED ao iniciar
  for (int i = 0; i < 5; i++)
  {
    ledcWrite(7, 20);
    delay(100);

    ledcWrite(7, 0);
    delay(100);
  }

  server.begin();

  Serial.println("Servidor iniciado");
}

void loop()
{
}


