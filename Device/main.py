#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi 手ぶくろ入力装置 メインプログラム
MPU6050角速度センサとHC-SR04距離センサを使用した非接触入力装置
"""

import time
from utils.sensors import MPU6050, HCSR04, AirTapDetector, RangeTimer
from utils.gpio_controller import GPIOController
from config import LOOP_DT


class GloveInputDevice:
    """手ぶくろ入力装置メインクラス"""

    def __init__(self):
        print("手ぶくろ入力装置を初期化しています...")

        # GPIO制御を初期化
        self.gpio_controller = GPIOController()

        # センサーとコントローラーの初期化
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

                # 非ブロッキングLED制御の更新
                led_just_turned_off = self.gpio_controller.update_distance_leds()

                # LED消灯直後にエアタップ履歴をクリア
                if led_just_turned_off:
                    self.air_tap_detector.clear_history()

                # ジャイロセンサー値を取得
                gx, gy, gz = self.mpu6050.read_gyro()

                # ジャイロセンサー値に応じてLEDを制御
                self.gpio_controller.set_gyro_leds(gx, gy, gz)

                # 距離測定
                distance = self.hcsr04.measure_distance()

                if distance is not None:
                    # エアタップ検出
                    self.air_tap_detector.add_distance(distance)
                    air_tap_detected = self.air_tap_detector.check_air_tap()

                    if air_tap_detected:
                        # 距離レンジLEDが点灯中の場合は強制消灯
                        if self.gpio_controller.led_active:
                            self.gpio_controller.led_active = False
                            self.gpio_controller.set_distance_leds(0)

                        self.gpio_controller.blink_red()
                        self.air_tap_detector.clear_history()
                    else:
                        # 距離レンジ測定（エアタップが検出されなかった場合のみ）
                        range_value = self.gpio_controller.get_distance_range(distance)

                        # 距離レンジが同一である継続時間が1秒以上の場合
                        if self.range_timer.update(range_value, t_now):
                            # 範囲外はスキップ
                            if range_value < 0:
                                continue
                            # 点滅中でない場合のみLEDを点灯
                            if not self.gpio_controller.blink_active:
                                self.gpio_controller.set_distance_leds_non_blocking(
                                    range_value
                                )
                            # 距離レンジの継続時間をリセット
                            self.range_timer.reset_timer()

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
