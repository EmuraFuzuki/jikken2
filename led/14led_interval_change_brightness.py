import gpiozero
import time
import math


class LED:
    def __init__(self, pin, frequency=1000):
        """PWMLEDを使用して明るさ制御可能なLEDクラス"""
        self.device = gpiozero.PWMLED(pin, frequency=frequency)

    def fade_in(self, duration=2.0, steps=100):
        """LEDを徐々に明るくする（フェードイン）"""
        print(f"フェードイン開始 - {duration:.1f}秒かけて徐々に明るくします")
        step_time = duration / steps
        for i in range(steps + 1):
            brightness = i / steps  # 0.0から1.0まで
            self.device.value = brightness
            print(f"明るさ: {brightness:.2f} ({i + 1}/{steps + 1})", end="\r")
            time.sleep(step_time)
        print("\nフェードイン完了")

    def fade_out(self, duration=2.0, steps=100):
        """LEDを徐々に暗くする（フェードアウト）"""
        print(f"フェードアウト開始 - {duration:.1f}秒かけて徐々に暗くします")
        step_time = duration / steps
        for i in range(steps + 1):
            brightness = 1.0 - (i / steps)  # 1.0から0.0まで
            self.device.value = brightness
            print(f"明るさ: {brightness:.2f} ({i + 1}/{steps + 1})", end="\r")
            time.sleep(step_time)
        print("\nフェードアウト完了")

    def breathing_effect(self, duration=10.0, cycle_time=3.0):
        """呼吸のような明るさの変化（サイン波）"""
        print(
            f"呼吸効果開始 - {duration:.1f}秒間、{cycle_time:.1f}秒周期で明るさが変化します"
        )
        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            # サイン波を使って滑らかな明るさ変化を作成
            brightness = (math.sin(2 * math.pi * elapsed / cycle_time) + 1) / 2
            self.device.value = brightness
            print(f"明るさ: {brightness:.2f}", end="\r")
            time.sleep(0.05)  # 50ms間隔で更新
        print("\n呼吸効果完了")

    def pulse_effect(self, duration=8.0, pulse_width=1.0):
        """パルス効果 - 急速に明るくなって徐々に暗くなる"""
        print(f"パルス効果開始 - {duration:.1f}秒間、{pulse_width:.1f}秒周期でパルス")
        start_time = time.time()
        while time.time() - start_time < duration:
            # 急速にフェードイン
            self.fade_in(duration=pulse_width * 0.2, steps=20)
            # ゆっくりフェードアウト
            self.fade_out(duration=pulse_width * 0.8, steps=40)
            time.sleep(0.5)  # パルス間の待機時間
        print("パルス効果完了")

    def set_brightness(self, brightness):
        """明るさを直接設定（0.0-1.0）"""
        brightness = max(0.0, min(1.0, brightness))  # 0.0-1.0の範囲に制限
        self.device.value = brightness
        print(f"明るさを {brightness:.2f} に設定")

    def turn_off(self):
        """LEDを消灯"""
        self.device.off()
        print("LED消灯")


def main():
    led = LED(23, frequency=1000)  # LEDのピン番号とPWM周波数を設定

    print("LED明るさ制御実験を開始します。")
    print("PWMを使用してLEDの明るさを徐々に変化させます。\n")

    try:
        # 1. 基本的なフェードイン・フェードアウト
        print("=== 1. フェードイン・フェードアウト ===")
        input("Enterキーを押してフェードインを開始...")
        led.fade_in(duration=3.0)
        time.sleep(1)

        input("Enterキーを押してフェードアウトを開始...")
        led.fade_out(duration=3.0)
        time.sleep(1)

        # 2. 呼吸効果
        print("\n=== 2. 呼吸効果（サイン波） ===")
        input("Enterキーを押して呼吸効果を開始...")
        led.breathing_effect(duration=10.0, cycle_time=2.5)
        time.sleep(1)

        # 3. パルス効果
        print("\n=== 3. パルス効果 ===")
        input("Enterキーを押してパルス効果を開始...")
        led.pulse_effect(duration=8.0, pulse_width=1.5)
        time.sleep(1)

        # 4. 手動明るさ制御
        print("\n=== 4. 手動明るさ制御 ===")
        brightness_levels = [0.0, 0.2, 0.5, 0.8, 1.0, 0.5, 0.0]
        for brightness in brightness_levels:
            led.set_brightness(brightness)
            time.sleep(1.5)

        # 5. 高速フェード
        print("\n=== 5. 高速フェード ===")
        input("Enterキーを押して高速フェードを開始...")
        for _ in range(3):
            led.fade_in(duration=0.5, steps=25)
            led.fade_out(duration=0.5, steps=25)

    except KeyboardInterrupt:
        print("\n実験を中断しました。")
    finally:
        led.turn_off()
        print("実験終了")


if __name__ == "__main__":
    main()
