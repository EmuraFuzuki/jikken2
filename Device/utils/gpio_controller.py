#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPIO制御関連のクラス
"""

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None
    print(
        "Warning: RPi.GPIO module not found. This module is required for Raspberry Pi."
    )

import time
from config import (
    OUTPUT_LEDS,
    LED_GYRO_X,
    LED_GYRO_Y,
    LED_GYRO_Z,
    LED_DIST_1,
    LED_DIST_2,
    LED_DIST_3,
    GYRO_THRESHOLD,
    BLINK_TIMES,
    BLINK_INTERVAL,
    DISTANCE_RANGES,
    LED_ON_TIME,
)


class GPIOController:
    """GPIO制御クラス"""

    def __init__(self):
        if GPIO is None:
            print(
                "Warning: GPIO module not available. GPIO operations will be skipped."
            )
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # LED設定
        for pin in OUTPUT_LEDS:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        # 非ブロッキングLED制御用の変数
        self.led_end_time = 0
        self.led_active = False

    def set_gyro_leds(self, gx, gy, gz):
        """ジャイロセンサーの値に応じてLEDを制御"""
        if GPIO is None:
            return

        GPIO.output(LED_GYRO_X, GPIO.HIGH if abs(gx) >= GYRO_THRESHOLD else GPIO.LOW)
        GPIO.output(LED_GYRO_Y, GPIO.HIGH if abs(gy) >= GYRO_THRESHOLD else GPIO.LOW)
        GPIO.output(LED_GYRO_Z, GPIO.HIGH if abs(gz) >= GYRO_THRESHOLD else GPIO.LOW)

    def set_distance_leds(self, rng):
        """距離レンジに応じてLEDを制御 rng: 0=None,1,2,3"""
        if GPIO is None:
            return

        leds = (LED_DIST_1, LED_DIST_2, LED_DIST_3)
        for i, pin in enumerate(leds, start=1):
            GPIO.output(pin, GPIO.HIGH if rng and i <= rng else GPIO.LOW)

    def set_distance_leds_timed(self, rng, duration=LED_ON_TIME):
        """距離レンジに応じてLEDを指定時間点灯"""
        if GPIO is None:
            return

        leds = (LED_DIST_1, LED_DIST_2, LED_DIST_3)
        # LEDを点灯
        for i, pin in enumerate(leds, start=1):
            GPIO.output(pin, GPIO.HIGH if rng and i <= rng else GPIO.LOW)

        # 指定時間待機
        time.sleep(duration)

        # LEDを消灯
        for pin in leds:
            GPIO.output(pin, GPIO.LOW)

    def set_distance_leds_non_blocking(self, rng, duration=LED_ON_TIME):
        """距離レンジに応じてLEDを非ブロッキングで指定時間点灯"""
        if GPIO is None:
            return

        leds = (LED_DIST_1, LED_DIST_2, LED_DIST_3)
        # LEDを点灯
        for i, pin in enumerate(leds, start=1):
            GPIO.output(pin, GPIO.HIGH if rng and i <= rng else GPIO.LOW)

        # 終了時刻を設定
        self.led_end_time = time.time() + duration
        self.led_active = True

    def update_distance_leds(self):
        """非ブロッキングLED制御の更新（メインループから呼び出し）"""
        if GPIO is None:
            return False

        if self.led_active and time.time() >= self.led_end_time:
            # LEDを消灯
            leds = (LED_DIST_1, LED_DIST_2, LED_DIST_3)
            for pin in leds:
                GPIO.output(pin, GPIO.LOW)
            self.led_active = False
            return True  # LED消灯完了を通知
        return False  # まだLED点灯中または非アクティブ

    def blink_red(self, times=BLINK_TIMES):
        """赤色LEDを点滅させる"""
        if GPIO is None:
            return

        for _ in range(times):
            for pin in (LED_DIST_1, LED_DIST_2, LED_DIST_3):
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(BLINK_INTERVAL)
            for pin in (LED_DIST_1, LED_DIST_2, LED_DIST_3):
                GPIO.output(pin, GPIO.LOW)
            time.sleep(BLINK_INTERVAL)

    def cleanup(self):
        """GPIO クリーンアップ"""
        if GPIO is None:
            return
        GPIO.cleanup()

    @staticmethod
    def get_distance_range(distance):
        """距離を範囲に変換（設定ファイルから読み込み）"""
        if distance is None:
            return None

        for range_config in DISTANCE_RANGES:
            if range_config["min"] <= distance < range_config["max"]:
                return range_config["level"]

        # 全ての範囲外（遠距離）の場合
        return 4  # 範囲外の遠距離として4を返す
