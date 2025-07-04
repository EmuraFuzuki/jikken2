import gpiozero
import time

LED_PIN = 23

led = gpiozero.DigitalOutputDevice(LED_PIN)
led.on()
status = True
while True:
    time.sleep(1)  # LEDを点灯したまま1秒待機
    if status:
        led.off()
        status = False
    else:
        led.on()
        status = True
