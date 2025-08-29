# 🩺 Sistema IoT de Detección de Caídas con Alerta en Telegram

Este proyecto consiste en un **dispositivo portátil de bajo costo** diseñado para monitorear en tiempo real posibles caídas de pacientes, adultos mayores o personas en riesgo.  
Cuando se detecta una caída, se activa una **alarma sonora y visual** y se envía una **notificación inmediata a un grupo de Telegram**, permitiendo una respuesta rápida de familiares o cuidadores.  

---

## 🚀 Características principales
- ✅ **Detección automática de caídas** con acelerómetro ADXL345.  
- ✅ **Botón de pánico** para activar la alarma manualmente.  
- ✅ **Botón de apagado con retardo (5s)** para evitar falsas desactivaciones.  
- ✅ **Alerta sonora y visual** mediante buzzer y LED.  
- ✅ **Integración con Telegram Bot** para enviar notificaciones instantáneas.  
- ✅ **Sistema económico y replicable**, pensado para aplicaciones en medicina y cuidado de adultos mayores.  

---

## 🛠️ Componentes utilizados
- Raspberry Pi 3  
- Acelerómetro **ADXL345** (I²C)  
- 2 botones (pánico y apagado)  
- 1 LED (alerta visual)  
- 1 buzzer (alerta sonora)  
- Resistencias y cableado básico  

### Librerías de Python
- `RPi.GPIO`
- `time`
- `asyncio`
- `board`
- `busio`
- `adafruit_adxl34x`
- `python-telegram-bot`

## 🔌 Esquema de conexiones
- **LED** → Pin GPIO 18 + resistencia a GND  
- **Buzzer** → Pin GPIO 23 + GND  
- **Botón de apagado** → Pin GPIO 24 + GND  
- **Botón de pánico** → Pin GPIO 25 + GND  
- **Acelerómetro ADXL345**:  
  - VCC → 3.3V  
  - GND → GND  
  - SDA → Pin GPIO 2 (SDA)  
  - SCL → Pin GPIO 3 (SCL)  
