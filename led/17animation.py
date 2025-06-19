import sys

sys.path.append("..")
from mod.led import LED
import time
import threading

# 使用可能なGPIOピン
USABLE_GPIOS = [2, 3, 4, 17]


class LEDAnimation:
    """
    4つのLEDを使ったアニメーションクラス
    """

    def __init__(self, pins=None):
        """
        LEDアニメーションクラスの初期化

        Args:
            pins (list): 使用するGPIOピンのリスト（デフォルト: USABLE_GPIOS）
        """
        if pins is None:
            pins = USABLE_GPIOS

        self.pins = pins
        self.leds = []

        # 各ピンにLEDオブジェクトを作成
        for pin in self.pins:
            self.leds.append(LED(pin=pin))

        print(f"4つのLEDが初期化されました: ピン番号 {self.pins}")

    def all_off(self):
        """全てのLEDを消灯"""
        for led in self.leds:
            led.off()

    def all_on(self):
        """全てのLEDを点灯"""
        for led in self.leds:
            led.on()

    def wave_animation(self, duration=10.0, speed=0.3):
        """
        波のようなアニメーション
        左から右へ順番に点灯していくパターン

        Args:
            duration (float): アニメーションの継続時間（秒）
            speed (float): 点灯間隔（秒）
        """
        print("波アニメーションを開始します...")
        start_time = time.time()

        while time.time() - start_time < duration:
            # 左から右へ
            for i, led in enumerate(self.leds):
                self.all_off()
                led.on()
                time.sleep(speed)

            # 右から左へ
            for i in range(len(self.leds) - 1, -1, -1):
                self.all_off()
                self.leds[i].on()
                time.sleep(speed)

        self.all_off()
        print("波アニメーション終了")

    def chase_animation(self, duration=10.0, speed=0.2):
        """
        追いかけアニメーション
        一度に複数のLEDが点灯して移動するパターン

        Args:
            duration (float): アニメーションの継続時間（秒）
            speed (float): 移動間隔（秒）
        """
        print("追いかけアニメーションを開始します...")
        start_time = time.time()

        while time.time() - start_time < duration:
            for i in range(len(self.leds)):
                self.all_off()
                # 現在と次のLEDを点灯
                self.leds[i].on()
                if i + 1 < len(self.leds):
                    self.leds[i + 1].on()
                time.sleep(speed)

        self.all_off()
        print("追いかけアニメーション終了")

    def breathing_sync(self, duration=10.0, cycle_time=2.0):
        """
        全てのLEDが同期して呼吸するアニメーション

        Args:
            duration (float): アニメーションの継続時間（秒）
            cycle_time (float): 呼吸の1サイクル時間（秒）
        """
        print("同期呼吸アニメーションを開始します...")

        # 全てのLEDで同時に呼吸効果を開始（スレッドで並列実行）
        threads = []
        for led in self.leds:
            thread = threading.Thread(
                target=led.breathing_effect, args=(duration, cycle_time)
            )
            thread.start()
            threads.append(thread)

        # 全てのスレッドの終了を待機
        for thread in threads:
            thread.join()

        self.all_off()
        print("同期呼吸アニメーション終了")

    def random_twinkle(self, duration=10.0):
        """
        ランダムにきらめくアニメーション

        Args:
            duration (float): アニメーションの継続時間（秒）
        """
        import random

        print("きらめきアニメーションを開始します...")
        start_time = time.time()

        while time.time() - start_time < duration:
            # ランダムにLEDを選択
            led_index = random.randint(0, len(self.leds) - 1)
            led = self.leds[led_index]

            # 短時間点灯
            led.on()
            time.sleep(0.1)
            led.off()
            time.sleep(random.uniform(0.1, 0.5))

        self.all_off()
        print("きらめきアニメーション終了")

    def fade_wave(self, duration=10.0, fade_time=1.0):
        """
        フェードを使った波アニメーション

        Args:
            duration (float): アニメーションの継続時間（秒）
            fade_time (float): フェードの時間（秒）
        """
        print("フェード波アニメーションを開始します...")
        start_time = time.time()

        while time.time() - start_time < duration:
            # 各LEDを順番にフェードイン・アウト
            for led in self.leds:
                thread1 = threading.Thread(target=led.fade_in, args=(fade_time / 2, 20))
                thread2 = threading.Thread(
                    target=lambda: (
                        time.sleep(fade_time / 2),
                        led.fade_out(fade_time / 2, 20),
                    )
                )

                thread1.start()
                thread1.join()
                thread2.start()
                thread2.join()

        self.all_off()
        print("フェード波アニメーション終了")

    def demo_all_animations(self):
        """全てのアニメーションを順番にデモ実行"""
        print("=== LEDアニメーションデモ開始 ===")

        # 初期化確認
        print("\n全てのLEDを一度点灯してテストします...")
        self.all_on()
        time.sleep(1)
        self.all_off()
        time.sleep(1)

        # 各アニメーションを実行
        self.wave_animation(duration=8.0)
        time.sleep(1)

        self.chase_animation(duration=8.0)
        time.sleep(1)

        self.random_twinkle(duration=8.0)
        time.sleep(1)

        self.breathing_sync(duration=6.0, cycle_time=1.5)
        time.sleep(1)

        self.fade_wave(duration=8.0)

        print("\n=== LEDアニメーションデモ終了 ===")

    def close(self):
        """全てのLEDリソースを解放"""
        for led in self.leds:
            led.close()
        print("LEDリソースが解放されました")


def main():
    """メイン実行関数"""
    # LEDアニメーションオブジェクトを作成
    animation = LEDAnimation()

    try:
        # デモ実行
        animation.demo_all_animations()

    except KeyboardInterrupt:
        print("\nプログラムが中断されました")

    finally:
        # リソースを確実に解放
        animation.close()


if __name__ == "__main__":
    main()
