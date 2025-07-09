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
        """距離を範囲に変換"""
        if distance is None:
            return None
        elif 0.0 <= distance < 5.0:
            return 1
        elif 5.0 <= distance < 10.0:
            return 2
        elif 10.0 <= distance < 15.0:
            return 3
        else:
            return None
