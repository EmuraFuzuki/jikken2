#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi 手ぶくろ入力装置
  - MPU6050 角速度トリガ
  - HC-SR04 距離レンジ & エアタップ検出
"""

import smbus
import time
import RPi.GPIO as GPIO
from collections import deque

# ------------------------------------------------------------
# GPIO 設定
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_GYRO_X = 17  # 黄
LED_GYRO_Y = 27  # 青
LED_GYRO_Z = 22  # 緑
LED_DIST_1 = 5  # 赤1
LED_DIST_2 = 6  # 赤2
LED_DIST_3 = 13  # 赤3

TRIG_PIN = 23
ECHO_PIN = 24

OUTPUT_LEDS = [LED_GYRO_X, LED_GYRO_Y, LED_GYRO_Z, LED_DIST_1, LED_DIST_2, LED_DIST_3]

for pin in OUTPUT_LEDS:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO_PIN, GPIO.IN)

# ------------------------------------------------------------
# MPU6050 定数
I2C_BUS = 1
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_THRESHOLD = 150.0  # [°/s] しきい値
GYRO_SCALE = 131.0  # ±250°/s モード

# 初期化
bus = smbus.SMBus(I2C_BUS)
bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)  # スリープ解除
time.sleep(0.1)


def read_gyro():
    def _read_word(reg):
        high = bus.read_byte_data(MPU_ADDR, reg)
        low = bus.read_byte_data(MPU_ADDR, reg + 1)
        val = (high << 8) | low
        return val - 65536 if val & 0x8000 else val

    gx = _read_word(GYRO_XOUT_H) / GYRO_SCALE
    gy = _read_word(GYRO_XOUT_H + 2) / GYRO_SCALE
    gz = _read_word(GYRO_XOUT_H + 4) / GYRO_SCALE
    return gx, gy, gz


# ------------------------------------------------------------
# 距離測定 (HC-SR04)
SOUND_SPEED = 34300.0  # [cm/s]


def measure_distance(timeout=0.03):
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


# ------------------------------------------------------------
# エアタップ検出用パラメータ
TAP_WINDOW = 0.30  # [s] 観測窓
TAP_NEAR = 5.0  # [cm] 近距離しきい
TAP_FAR = 10.0  # [cm] 遠距離しきい
BLINK_TIMES = 3
BLINK_INTERVAL = 0.15  # [s]

dist_history = deque(maxlen=10)


def check_air_tap():
    """履歴からエアタップを判定"""
    if len(dist_history) < 2:
        return False
    # シンプルな山検出: 遠→近→遠 で min<near, max>far
    distances = list(dist_history)
    d_min = min(distances)
    d_max = max(distances)
    return d_min < TAP_NEAR and d_max > TAP_FAR


def blink_red(times=BLINK_TIMES):
    for _ in range(times):
        for pin in (LED_DIST_1, LED_DIST_2, LED_DIST_3):
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(BLINK_INTERVAL)
        for pin in (LED_DIST_1, LED_DIST_2, LED_DIST_3):
            GPIO.output(pin, GPIO.LOW)
        time.sleep(BLINK_INTERVAL)


# ------------------------------------------------------------
# 距離レンジ管理
class RangeTimer:
    def __init__(self, hold_sec=1.0):
        self.hold_sec = hold_sec
        self.current_range = None
        self.enter_time = None

    def update(self, rng, now):
        """rng: 0=None,1(0-5),2(5-10),3(10-15)"""
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


range_timer = RangeTimer(hold_sec=1.0)


def set_distance_leds(rng):
    """rng: 0=None,1,2,3"""
    leds = (LED_DIST_1, LED_DIST_2, LED_DIST_3)
    for i, pin in enumerate(leds, start=1):
        GPIO.output(pin, GPIO.HIGH if rng and i <= rng else GPIO.LOW)


# ------------------------------------------------------------
# メインループ
try:
    LOOP_DT = 0.05  # 20 Hz
    while True:
        t_now = time.time()

        # --- ジャイロ処理 ---
        gx, gy, gz = read_gyro()
        GPIO.output(LED_GYRO_X, GPIO.HIGH if abs(gx) >= GYRO_THRESHOLD else GPIO.LOW)
        GPIO.output(LED_GYRO_Y, GPIO.HIGH if abs(gy) >= GYRO_THRESHOLD else GPIO.LOW)
        GPIO.output(LED_GYRO_Z, GPIO.HIGH if abs(gz) >= GYRO_THRESHOLD else GPIO.LOW)

        # --- 距離測定 ---
        dist = measure_distance()
        if dist is not None:
            dist_history.appendleft(dist)  # 新しい測定を左側へ
            # エアタップ判定
            if check_air_tap():
                blink_red()
                dist_history.clear()  # 同一タップの再検出防止
            # 距離レンジ決定
            if 0.0 <= dist < 5.0:
                rng = 1
            elif 5.0 <= dist < 10.0:
                rng = 2
            elif 10.0 <= dist < 15.0:
                rng = 3
            else:
                rng = None
            if range_timer.update(rng, t_now):
                set_distance_leds(rng)
        else:
            # 測定失敗時は無視
            pass

        time.sleep(LOOP_DT)

except KeyboardInterrupt:
    print("\n終了要求を受信しました。GPIO をクリーンアップします。")
finally:
    GPIO.cleanup()
