import RPi.GPIO as GPIO
import time
import asyncio
import board
import busio
import adafruit_adxl34x
from telegram import Bot

# ==== CONFIGURACIÓN DE PINES ====
LED_PIN = 18
BUZZER_PIN = 23
BUTTON_OFF_PIN = 12    # Botón para apagar alarma
BUTTON_PANIC_PIN = 25    # Botón de pánico

# ==== CONFIGURACIÓN TELEGRAM ====
TOKEN = "8025517428:AAFiA4xXMk1Z8awDiKCrb5w43x_3YzTqfkQ"
CHAT_ID = -4957824265

# ==== CONFIGURACIÓN DE SENSOR ====
i2c = busio.I2C(board.SCL, board.SDA)  
sensor = adafruit_adxl34x.ADXL345(i2c)

# Estado de la alarma
alarma_activa = False
tiempo_alarma_activada = 0  # para controlar el retardo de apagado

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_OFF_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_PANIC_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def leer_acelerometro():
    x, y, z = sensor.acceleration
    return {"x": x, "y": y, "z": z}

def detectar_caida():
    accel = leer_acelerometro()
    if abs(accel['x']) > 19 or abs(accel['y']) > 19 or abs(accel['z']) > 19:
        return True, accel
    return False, accel

def boton_apagar_presionado():
    return GPIO.input(BUTTON_OFF_PIN) == GPIO.LOW

def boton_panico_presionado():
    return GPIO.input(BUTTON_PANIC_PIN) == GPIO.LOW

def activar_alarma():
    GPIO.output(LED_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def desactivar_alarma():
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

async def enviar_alerta(mensaje):
    bot = Bot(token=TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=mensaje)
        print("📢 Alerta enviada por Telegram")
    except Exception as e:
        print(f"❌ Error enviando alerta: {e}")

def loop():
    global alarma_activa, tiempo_alarma_activada
    try:
        while True:
            caida_detectada, accel_data = detectar_caida()
            
            # Si hay caída y la alarma no está activa
            if caida_detectada and not alarma_activa:
                alarma_activa = True
                tiempo_alarma_activada = time.time()
                print("⚠️ ALERTA: Posible caída detectada")
                activar_alarma()
                mensaje = (f"🚨 ALERTA DE CAÍDA DETECTADA\n")
                           
                asyncio.run(enviar_alerta(mensaje))
                time.sleep(2)

            # Si se presiona el botón de pánico y la alarma no está activa
            if boton_panico_presionado() and not alarma_activa:
                alarma_activa = True
                tiempo_alarma_activada = time.time()
                print("🆘 BOTÓN DE PÁNICO ACTIVADO")
                activar_alarma()
                asyncio.run(enviar_alerta("🆘 BOTÓN DE PÁNICO ACTIVADO"))
                time.sleep(1)

            # Si la alarma está activa y se presiona el botón de apagado (con retardo de 5 s)
            if alarma_activa and boton_apagar_presionado():
                if time.time() - tiempo_alarma_activada >= 5:
                    alarma_activa = False
                    desactivar_alarma()
                    print("✅ Alarma desactivada manualmente")
                    asyncio.run(enviar_alerta("✅ Todo está bien, falsa alarma"))
                    time.sleep(1)  # evitar rebotes
                else:
                    print("⏳ Espera 5 segundos antes de apagar la alarma")

            # Si no hay caída y la alarma no está activa
            if not alarma_activa:
                desactivar_alarma()
                
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nPrograma detenido")

if __name__ == "__main__":
    setup()
    loop()
