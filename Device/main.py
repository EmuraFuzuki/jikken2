#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi 手ぶくろ入力装置 メインプログラム
    - MPU6050 角速度トリガ
    - HC-SR04 距離レンジ & エアタップ検出
"""

import time
from utils.sensors import MPU6050, HCSR04, AirTapDetector, RangeTimer
from utils.gpio_controller import GPIOController
from config import LOOP_DT


class GloveInputDevice:
    """手ぶくろ入力装置メインクラス"""

    def __init__(self):
        print("手ぶくろ入力装置を初期化しています...")

        # GPIO制御を最初に初期化（GPIO.setmode()を実行）
        self.gpio_controller = GPIOController()

        # その後でセンサーとコントローラーの初期化
        self.mpu6050 = MPU6050()
        self.hcsr04 = HCSR04()
        self.air_tap_detector = AirTapDetector()
        self.range_timer = RangeTimer()

        print("初期化完了")

    def run(self):
        """メインループ実行"""
        print("手ぶくろ入力装置を開始します...")
        print("Ctrl+C で終了します")

        try:
            while True:
                t_now = time.time()

                # ジャイロセンサーの値を取得
                gx, gy, gz = self.mpu6050.read_gyro()

                # ジャイロセンサーの値に応じてLEDを制御
                self.gpio_controller.set_gyro_leds(gx, gy, gz)

                # 距離測定
                distance = self.hcsr04.measure_distance()

                if distance is not None:
                    # 1. エアタップ検出
                    self.air_tap_detector.add_distance(distance)
                    air_tap_detected = self.air_tap_detector.check_air_tap()

                    if air_tap_detected:
                        print(f"エアタップ検出！ 距離: {distance:.1f} cm")
                        self.gpio_controller.blink_red()
                        self.air_tap_detector.clear_history()
                        # エアタップ検出時は距離レンジ処理をスキップ
                    else:
                        # 2. 距離レンジ測定（エアタップが検出されなかった場合のみ）
                        range_value = self.gpio_controller.get_distance_range(distance)

                        # 3. 距離レンジが同一である継続時間が1秒以上の場合
                        if self.range_timer.update(range_value, t_now):
                            print(f"距離レンジ: {range_value}, 距離: {distance:.1f} cm")
                            # LEDを1秒間点灯
                            self.gpio_controller.set_distance_leds_timed(range_value)
                            # 距離レンジの継続時間をリセット
                            self.range_timer.reset_timer()

                # デバッグ出力（必要に応じて）
                # print(
                #     f"Gyro: X={gx:.1f}, Y={gy:.1f}, Z={gz:.1f}, Distance={distance if distance else 'None'}"
                # )

                time.sleep(LOOP_DT)

        except KeyboardInterrupt:
            print("\n終了要求を受信しました。")
        finally:
            self.cleanup()

    def cleanup(self):
        """リソースのクリーンアップ"""
        print("GPIO をクリーンアップします。")
        self.gpio_controller.cleanup()
        print("終了しました。")


def main():
    """メイン関数"""
    device = GloveInputDevice()
    device.run()


if __name__ == "__main__":
    main()
