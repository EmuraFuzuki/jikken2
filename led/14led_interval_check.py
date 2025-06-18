import gpiozero
import time


class LED:
    def __init__(self, pin, interval=1.0, time_length=3.0):
        self.device = gpiozero.DigitalOutputDevice(pin)
        self.interval = interval
        self.time_length = time_length

    def toggle_led(self, time_length=None, interval=None):
        """LEDを指定した間隔で点滅させる関数"""
        if time_length is not None:
            self.time_length = time_length
        if interval is not None:
            self.interval = interval
        self.show_interval()
        end_time = time.time() + self.time_length
        while time.time() < end_time:
            self.device.on()
            time.sleep(self.interval)
            self.device.off()
            time.sleep(self.interval)

    def show_interval(self):
        """LEDの点滅間隔を表示する関数"""
        frequency = 1 / (2 * self.interval)  # 周波数を計算
        print(
            f"LED点滅: 間隔 {self.interval:.3f}秒, 周波数 {frequency:.1f}Hz, 継続時間 {self.time_length:.1f}秒"
        )


def main():
    led = LED(23, interval=1.0, time_length=5.0)  # LEDのピン番号と初期点滅間隔を設定

    # 人が点滅を検知できなくなる閾値を調べるための間隔リスト
    # 0.5秒から0.01秒まで段階的に細かくして、最後に非常に高い周波数をテスト
    intervals = [
        1.0,  # 1秒間隔 - 明確に点滅が見える
        0.5,  # 0.5秒間隔 - 点滅が見える
        0.2,  # 0.2秒間隔 - 点滅が見える
        0.1,  # 0.1秒間隔 - 点滅が見える
        0.08,  # 0.08秒間隔 - 12.5Hz
        0.06,  # 0.06秒間隔 - 16.7Hz
        0.05,  # 0.05秒間隔 - 20Hz（閾値付近）
        0.04,  # 0.04秒間隔 - 25Hz（閾値付近）
        0.033,  # 0.033秒間隔 - 30Hz（閾値付近）
        0.025,  # 0.025秒間隔 - 40Hz
        0.02,  # 0.02秒間隔 - 50Hz
        0.016,  # 0.016秒間隔 - 60Hz
        0.01,  # 0.01秒間隔 - 100Hz
        0.005,  # 0.005秒間隔 - 200Hz
        0.001,  # 0.001秒間隔 - 1000Hz（ほぼ常時点灯に見える）
    ]

    print("LED点滅検知実験を開始します。")
    print("各間隔で点滅させ、どの程度の速さで点滅が見えなくなるかを確認してください。")
    print("一般的に20-30Hz（0.033-0.05秒間隔）付近で点滅を認識できなくなります。\n")

    for i, interval in enumerate(intervals, 1):
        frequency = 1 / (2 * interval)  # 周波数を計算（Hz）
        print(
            f"\n実験 {i}/{len(intervals)}: 間隔 {interval:.3f}秒 (周波数: {frequency:.1f}Hz)"
        )
        input("Enterキーを押して開始...")
        led.toggle_led(interval=interval)
        time.sleep(2)  # 次の実験まで少し待機


if __name__ == "__main__":
    main()
