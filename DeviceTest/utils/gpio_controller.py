#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPIO制御関連のクラス
"""

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

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
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # LED設定
        for pin in OUTPUT_LEDS:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        # 非ブロッキングLED制御用の変数
        self.led_end_time = 0
        self.led_active = False

        # 非ブロッキング点滅制御用の変数
        self.blink_active = False
        self.blink_count = 0
        self.blink_max_count = 0
        self.blink_next_time = 0
        self.blink_state = False  # True: 点灯, False: 消灯

    def set_gyro_leds(self, gx, gy, gz):
        """ジャイロセンサー値に応じてLEDを制御（最大角速度の軸のみ点灯）"""
        if GPIO is None:
            return

        # 全ての軸の絶対値を取得
        abs_gx = abs(gx)
        abs_gy = abs(gy)
        abs_gz = abs(gz)

        # 最大角速度を取得
        max_gyro = max(abs_gx, abs_gy, abs_gz)

        # 閾値以上の場合のみ処理
        if max_gyro >= GYRO_THRESHOLD:
            # 最大角速度の軸のみ点灯
            GPIO.output(LED_GYRO_X, GPIO.HIGH if abs_gx == max_gyro else GPIO.LOW)
            GPIO.output(LED_GYRO_Y, GPIO.HIGH if abs_gy == max_gyro else GPIO.LOW)
            GPIO.output(LED_GYRO_Z, GPIO.HIGH if abs_gz == max_gyro else GPIO.LOW)
        else:
            # 全て消灯
            GPIO.output(LED_GYRO_X, GPIO.LOW)
            GPIO.output(LED_GYRO_Y, GPIO.LOW)
            GPIO.output(LED_GYRO_Z, GPIO.LOW)

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

        led_just_turned_off = False

        # 距離レンジLEDの更新
        if self.led_active and time.time() >= self.led_end_time:
            # LEDを消灯
            leds = (LED_DIST_1, LED_DIST_2, LED_DIST_3)
            for pin in leds:
                GPIO.output(pin, GPIO.LOW)
            self.led_active = False
            led_just_turned_off = True

        # 点滅制御の更新
        self.update_blink()

        return led_just_turned_off

    def blink_red(self, times=BLINK_TIMES):
        """赤色LEDを非ブロッキングで点滅させる"""
        if GPIO is None:
            return

        # 点滅制御の初期化
        self.blink_active = True
        self.blink_count = 0
        self.blink_max_count = times * 2  # 点灯・消灯を1セットとして2倍
        self.blink_next_time = time.time()
        self.blink_state = True  # 最初は点灯から開始

    def update_blink(self):
        """非ブロッキング点滅制御の更新"""
        if not self.blink_active or GPIO is None:
            return

        current_time = time.time()
        if current_time >= self.blink_next_time:
            if self.blink_state:
                # 点灯
                for pin in (LED_DIST_1, LED_DIST_2, LED_DIST_3):
                    GPIO.output(pin, GPIO.HIGH)
            else:
                # 消灯
                for pin in (LED_DIST_1, LED_DIST_2, LED_DIST_3):
                    GPIO.output(pin, GPIO.LOW)

            self.blink_count += 1
            self.blink_state = not self.blink_state
            self.blink_next_time = current_time + BLINK_INTERVAL

            # 点滅完了チェック
            if self.blink_count >= self.blink_max_count:
                self.blink_active = False
                # 最終的に全て消灯
                for pin in (LED_DIST_1, LED_DIST_2, LED_DIST_3):
                    GPIO.output(pin, GPIO.LOW)

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
        return -1  # 範囲外の遠距離として-1を返す
