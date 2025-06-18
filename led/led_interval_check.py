import gpiozero
import time


def main():
    LED_PIN = 23

    led = gpiozero.DigitalOutputDevice(LED_PIN)
    led.on()

    while True:
        time.sleep(1)  # LEDを点灯したまま1秒待機


if __name__ == "__main__":
    main()
