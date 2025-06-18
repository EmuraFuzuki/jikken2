import gpiozero
import time

LED_PIN = 23
led = gpiozero.DigitalOutputDevice(LED_PIN)


def toggle_led(time_length=10, interval=1):
    """LEDを指定した間隔で点滅させる関数"""
    end_time = time.time() + time_length
    while time.time() < end_time:
        led.on()
        time.sleep(interval)
        led.off()
        time.sleep(interval)


def main():
    toggle_led(time_length=10, interval=1)


if __name__ == "__main__":
    main()
