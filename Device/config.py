#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定ファイル - GPIO ピン番号と各種定数
"""

# GPIO ピン番号
LED_GYRO_X = 17  # 黄
LED_GYRO_Y = 27  # 青
LED_GYRO_Z = 22  # 緑
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
TAP_NEAR = 5.0  # [cm] 近距離しきい
TAP_FAR = 10.0  # [cm] 遠距離しきい
BLINK_TIMES = 3
BLINK_INTERVAL = 0.15  # [s]

# メインループ設定
LOOP_DT = 0.05  # 20 Hz
