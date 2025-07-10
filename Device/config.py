#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定ファイル - GPIO ピン番号と各種定数
"""

# GPIO ピン番号
LED_GYRO_X = 16  # 黄
LED_GYRO_Y = 20  # 青
LED_GYRO_Z = 21  # 緑
LED_DIST_1 = 5  # 赤1
LED_DIST_2 = 6  # 赤2
LED_DIST_3 = 13  # 赤3

TRIG_PIN = 23
ECHO_PIN = 24

OUTPUT_LEDS = [LED_GYRO_X, LED_GYRO_Y, LED_GYRO_Z, LED_DIST_1, LED_DIST_2, LED_DIST_3]

# MPU6050 定数
I2C_BUS = 1
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_THRESHOLD = 150.0  # [°/s] しきい値
GYRO_SCALE = 131.0  # ±250°/s モード

# 距離測定定数
SOUND_SPEED = 34300.0  # [cm/s]

# エアタップ検出用パラメータ
TAP_WINDOW = 0.30  # [s] 観測窓
TAP_DETECTION_RANGE = 10.0  # [cm] エアタップ検出範囲（0~10cm）
TAP_MIN_SPEED = 15.0  # [cm/s] 最小近づき速度
BLINK_TIMES = 3  # 点滅回数
BLINK_INTERVAL = 0.15  # [s] 点滅間隔

# 距離レンジ設定
DISTANCE_RANGES = [
    {"min": 0.0, "max": 5.0, "level": 1},  # レンジ1: 0-5cm
    {"min": 5.0, "max": 10.0, "level": 2},  # レンジ2: 5-10cm
    {"min": 10.0, "max": 15.0, "level": 3},  # レンジ3: 10-15cm
]
RANGE_HOLD_TIME = 1.0  # [s] レンジ継続時間
LED_ON_TIME = 1.0  # [s] LED点灯時間

# メインループ設定
LOOP_DT = 0.05  # 20 Hz
