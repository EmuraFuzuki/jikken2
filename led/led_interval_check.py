import gpiozero
import time


class LED:
    def __init__(self, pin, interval=1.0):
        self.device = gpiozero.DigitalOutputDevice(pin)
        self.interval = interval

    def toggle_led(self, time_length=None, interval=None):
        """LEDを指定した間隔で点滅させる関数"""
        if time_length is not None:
            self.time_length = time_length
        if interval is not None:
            self.interval = interval
        end_time = time.time() + self.time_length
        while time.time() < end_time:
            self.device.on()
            time.sleep(interval if interval is not None else self.interval)
            self.device.off()
            time.sleep(interval if interval is not None else self.interval)

    def show_interval(self):
        """LEDの点滅間隔を表示する関数"""
        print(f"LED is blinking every {self.interval:.2f} seconds.")


def main():
    led = LED(23, interval=1.0, time_length=3.0)  # LEDのピン番号と初期点滅間隔を設定
    for i in range(5):
        interval = 1 / (i + 1)  # 点滅時間を10秒に設定
        led.toggle_led(interval=interval)
        led.show_interval()


if __name__ == "__main__":
    main()
