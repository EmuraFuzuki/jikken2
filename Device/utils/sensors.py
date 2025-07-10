#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import (
    I2C_BUS,
    MPU_ADDR,
    PWR_MGMT_1,
    GYRO_XOUT_H,
    GYRO_SCALE,
    TRIG_PIN,
    ECHO_PIN,
    SOUND_SPEED,
    TAP_NEAR,
    TAP_FAR,
    RANGE_HOLD_TIME,
)

"""
センサー関連のクラス
"""

try:
    import smbus
except ImportError:
    smbus = None
    print("Warning: smbus module not found. This module is required for Raspberry Pi.")

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None
    print(
        "Warning: RPi.GPIO module not found. This module is required for Raspberry Pi."
    )

import time
from collections import deque


class MPU6050:
    """MPU6050 ジャイロセンサークラス"""

    def __init__(self):
        self.bus = smbus.SMBus(I2C_BUS)
        self.bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)  # スリープ解除
        time.sleep(0.1)

    def read_gyro(self):
        """ジャイロセンサーの値を読み取る"""
        try:

            def _read_word(reg):
                high = self.bus.read_byte_data(MPU_ADDR, reg)
                low = self.bus.read_byte_data(MPU_ADDR, reg + 1)
                val = (high << 8) | low
                return val - 65536 if val & 0x8000 else val

            gx = _read_word(GYRO_XOUT_H) / GYRO_SCALE
            gy = _read_word(GYRO_XOUT_H + 2) / GYRO_SCALE
            gz = _read_word(GYRO_XOUT_H + 4) / GYRO_SCALE
            return gx, gy, gz
        # 例外処理
        except Exception as e:
            print(f"Error reading MPU6050: {e}")
            return 0.0, 0.0, 0.0


class HCSR04:
    """HC-SR04 超音波距離センサークラス"""

    def __init__(self):
        GPIO.setup(TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ECHO_PIN, GPIO.IN)

    def measure_distance(self, timeout=0.03):
        """超音波距離 [cm] (timeout 秒で失敗時 None)"""
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(10e-6)  # 10 µs パルス
        GPIO.output(TRIG_PIN, GPIO.LOW)

        start_time = time.time()
        while GPIO.input(ECHO_PIN) == GPIO.LOW:
            if time.time() - start_time > timeout:
                return None
        pulse_start = time.time()

        while GPIO.input(ECHO_PIN) == GPIO.HIGH:
            if time.time() - pulse_start > timeout:
                return None
        pulse_end = time.time()

        pulse_len = pulse_end - pulse_start
        distance_cm = (pulse_len * SOUND_SPEED) / 2.0
        return distance_cm


class AirTapDetector:
    """エアタップ検出クラス"""

    def __init__(self):
        self.dist_history = deque(maxlen=10)

    def add_distance(self, distance):
        """距離履歴に追加"""
        self.dist_history.appendleft(distance)

    def check_air_tap(self):
        """履歴からエアタップを判定"""
        if len(self.dist_history) < 2:
            return False
        # シンプルな山検出: 遠→近→遠 で min<near, max>far
        distances = list(self.dist_history)
        d_min = min(distances)
        d_max = max(distances)
        return d_min < TAP_NEAR and d_max > TAP_FAR

    def clear_history(self):
        """履歴をクリア"""
        self.dist_history.clear()


class RangeTimer:
    """距離レンジ管理クラス"""

    def __init__(self, hold_sec=RANGE_HOLD_TIME):
        self.hold_sec = hold_sec
        self.current_range = None
        self.enter_time = None

    def update(self, rng, now):
        """rng: None,1(0-5),2(5-10),3(10-15),4(範囲外)"""
        if rng == self.current_range:
            # 継続中
            return (
                rng is not None
                and self.enter_time is not None
                and now - self.enter_time >= self.hold_sec
            )
        else:
            # レンジ移行
            self.current_range = rng
            self.enter_time = now
            return False

    def reset_timer(self):
        """継続時間をリセット"""
        self.enter_time = None
