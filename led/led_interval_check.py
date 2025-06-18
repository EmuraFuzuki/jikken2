import gpiozero
import time

LED_PIN = 23
led = gpiozero.DigitalOutputDevice(LED_PIN)


class LED:
    def __init__(self, pin, interval=1.0):
        self.device = gpiozero.DigitalOutputDevice(pin)
        self.interval = interval

    def toggle_led(self, time_length=10):
        """LEDを指定した間隔で点滅させる関数"""
        end_time = time.time() + time_length
        while time.time() < end_time:
            self.device.on()
            time.sleep(self.interval)
            self.device.off()
            time.sleep(self.interval)

    def show_interval(self):
        """LEDの点滅間隔を表示する関数"""
        print(f"LED is blinking every {self.interval:.2f} seconds.")


def main():
    led = LED(pin=LED_PIN)
    for i in range(5):
        time_length = 1 / (i + 1)  # 点滅時間を10秒に設定
        led.toggle_led(time_length=time_length)
        led.show_interval()


if __name__ == "__main__":
    main()
