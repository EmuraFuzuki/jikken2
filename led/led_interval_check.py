import gpiozero
import time


class LED:
    def __init__(self, pin, interval=1.0):
        self.device = gpiozero.DigitalOutputDevice(pin)
        self.interval = interval

    def toggle_led(self, time_length=10, interval=1.0):
        """LEDを指定した間隔で点滅させる関数"""
        end_time = time.time() + time_length
        while time.time() < end_time:
            self.device.on()
            time.sleep(interval)
            self.device.off()
            time.sleep(interval)

    def show_interval(self):
        """LEDの点滅間隔を表示する関数"""
        print(f"LED is blinking every {self.interval:.2f} seconds.")


def main():
    led = LED(23)
    for i in range(5):
        interval = 1 / (i + 1)  # 点滅時間を10秒に設定
        led.toggle_led(interval=interval)
        led.show_interval()


if __name__ == "__main__":
    main()
