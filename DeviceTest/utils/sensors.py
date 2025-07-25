#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
センサー制御クラス
MPU6050ジャイロセンサとHC-SR04超音波センサの制御
"""

from config import (
    I2C_BUS,
    MPU_ADDR,
    PWR_MGMT_1,
    GYRO_XOUT_H,
    GYRO_SCALE,
    TRIG_PIN,
    ECHO_PIN,
    SOUND_SPEED,
    TAP_DETECTION_RANGE,
    TAP_MIN_SPEED,
    RANGE_HOLD_TIME,
)

import time
from collections import deque

try:
    import smbus
except ImportError:
    smbus = None

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


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
        except Exception:
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
    """エアタップ検出クラス（手を近づける動作を速度基準で検出）"""

    def __init__(self):
        self.dist_history = deque(maxlen=10)  # 距離履歴
        self.time_history = deque(maxlen=10)  # 時刻履歴

    def add_distance(self, distance):
        """距離履歴に追加"""
        current_time = time.time()
        self.dist_history.appendleft(distance)
        self.time_history.appendleft(current_time)

    def check_air_tap(self):
        """履歴からエアタップを判定"""
        if len(self.dist_history) < 3:  # 最低3点のデータが必要
            return False

        distances = list(self.dist_history)
        times = list(self.time_history)

        # 全ての距離が検出範囲内にあるかチェック
        if not all(0 <= d <= TAP_DETECTION_RANGE for d in distances):
            return False

        # 手を近づける動きかチェック
        start_distance = distances[-1]  # 最も古い距離
        end_distance = distances[0]  # 最新の距離

        # 距離が減少していない場合はエアタップではない
        if start_distance <= end_distance:
            return False

        # 十分な距離変化があるかチェック（最低2cm以上近づく必要）
        distance_change = start_distance - end_distance
        if distance_change < 2.0:
            return False

        # 速度を計算して閾値をチェック
        total_time = times[0] - times[-1]

        if total_time <= 0:
            return False

        approach_speed = distance_change / total_time  # cm/s

        # 十分な速度で近づいているかチェック
        return approach_speed >= TAP_MIN_SPEED

    def clear_history(self):
        """履歴をクリア"""
        self.dist_history.clear()
        self.time_history.clear()


class RangeTimer:
    """距離レンジ管理クラス"""

    def __init__(self, hold_sec=RANGE_HOLD_TIME):
        self.hold_sec = hold_sec
        self.current_range = None
        self.enter_time = None
        self.last_triggered_range = None
        self.last_triggered_time = None

    def update(self, rng, now):
        """レンジの更新と判定
        rng: None,1(0-5),2(5-10),3(10-15),-1(範囲外)
        """
        if rng == self.current_range:
            # 同じレンジに継続中
            if (
                rng is not None
                and self.enter_time is not None
                and now - self.enter_time >= self.hold_sec
            ):
                # 前回トリガーされてから十分時間が経過しているかチェック
                if (
                    self.last_triggered_range != rng
                    or self.last_triggered_time is None
                    or now - self.last_triggered_time >= self.hold_sec
                ):
                    return True
            return False
        else:
            # レンジ移行
            self.current_range = rng
            self.enter_time = now
            return False

    def reset_timer(self):
        """継続時間をリセット（トリガー後に呼び出し）"""
        # トリガーされた情報を記録
        self.last_triggered_range = self.current_range
        self.last_triggered_time = time.time()
        # 新しい判定のためにenter_timeをリセット
        self.enter_time = time.time()
