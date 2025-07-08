以下に、要求仕様を満たす回路構成（配線図のテキスト説明）と Python 3 用ソースコード（実行ファイル 1 本）を示します。ハードウェアと GPIO 番号は一例ですので、環境に合わせて適宜変更してください。

---

## 1. 回路設計（配線一覧）

| 役割                | Raspberry Pi GPIO | 物理ピン番号 (40 pin) | 接続先                      | メモ                                    |
| ----------------- | ----------------- | --------------- | ------------------------ | ------------------------------------- |
| **I2C SDA**       | GPIO 2            | 3               | MPU6050 SDA              | 3.3 V系                                |
| **I2C SCL**       | GPIO 3            | 5               | MPU6050 SCL              | 3.3 V系                                |
| **Gyro LED X（黄）** | GPIO 17           | 11              | 黄 LED アノード               | カソード→330 Ω→GND                        |
| **Gyro LED Y（青）** | GPIO 27           | 13              | 青 LED アノード               | 同上                                    |
| **Gyro LED Z（緑）** | GPIO 22           | 15              | 緑 LED アノード               | 同上                                    |
| **距離 LED 1（赤1）**  | GPIO 5            | 29              | 赤 LED 1 アノード             | 330 Ω→GND                             |
| **距離 LED 2（赤2）**  | GPIO 6            | 31              | 赤 LED 2 アノード             | 330 Ω→GND                             |
| **距離 LED 3（赤3）**  | GPIO 13           | 33              | 赤 LED 3 アノード             | 330 Ω→GND                             |
| **HC-SR04 TRIG**  | GPIO 23           | 16              | 超音波 TRIG                 | 3.3 V系                                |
| **HC-SR04 ECHO**  | GPIO 24           | 18              | 超音波 ECHO（電圧分圧後）          | 5 V→1 kΩ→ECHO→2 kΩ→GND（分圧で 3.3 V 以下に） |
| **3.3 V**         | —                 | 1               | MPU6050 VCC, HC-SR04 VCC | —                                     |
| **GND**           | —                 | 9 など            | 全 GND                    | 共通グラウンド                               |

> **注意**
>
> * HC-SR04 の ECHO は 5 V 出力なので、必ず 1 kΩ/2 kΩ 等で 3.3 V 以下に分圧してください。
> * MPU6050 は 3.3 V 動作、I2C バスはラズパイ側のプルアップを利用。
> * LED には電流制限抵抗（220–330 Ω程度）を必ず挿入します。

---

## 2. 動作仕様とアルゴリズム

### 2.1 ジャイロ角速度入力

* MPU6050 の ±250 °/s フルスケールを使用（感度 131 LSB/(°/s)）。
* 各軸の絶対角速度が `GYRO_THRESHOLD [°/s]` を超えている間、その軸に対応する LED を点灯。

### 2.2 距離入力

1. **距離レンジ判定**

   * 連続測定で **1 秒以上** 同じレンジに留まった場合に確定。
   * 距離レンジと LED 数

     * 0 – 5 cm → 赤1 LED
     * 5 – 10 cm → 赤1+赤2
     * 10 – 15 cm → 赤1+赤2+赤3
   * 15 cm超またはレンジ未確定時は全赤 LED 消灯。
2. **エアタップ検出**

   * 直近 `TAP_WINDOW = 0.3 s` 内で 「距離が 10 cm超 → 5 cm未満 → 10 cm超」 の急変を検出。
   * 検出時、赤 LED 全点滅を `BLINK_TIMES` 回実行。
   * 距離レンジ LED 表示はブリンク終了後に再開。

---

## 3. Python ソースコード

以下を `gesture_input.py` など任意の名前で保存してください。
（ユーザーのご要望により *実行せず*、テキストのみで提供します。）

```python
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

LED_GYRO_X = 17   # 黄
LED_GYRO_Y = 27   # 青
LED_GYRO_Z = 22   # 緑
LED_DIST_1 = 5    # 赤1
LED_DIST_2 = 6    # 赤2
LED_DIST_3 = 13   # 赤3

TRIG_PIN = 23
ECHO_PIN = 24

OUTPUT_LEDS = [LED_GYRO_X, LED_GYRO_Y, LED_GYRO_Z,
               LED_DIST_1, LED_DIST_2, LED_DIST_3]

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
GYRO_THRESHOLD = 150.0        # [°/s] しきい値
GYRO_SCALE = 131.0            # ±250°/s モード

# 初期化
bus = smbus.SMBus(I2C_BUS)
bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)  # スリープ解除
time.sleep(0.1)

def read_gyro():
    def _read_word(reg):
        high = bus.read_byte_data(MPU_ADDR, reg)
        low  = bus.read_byte_data(MPU_ADDR, reg + 1)
        val  = (high << 8) | low
        return val - 65536 if val & 0x8000 else val

    gx = _read_word(GYRO_XOUT_H)     / GYRO_SCALE
    gy = _read_word(GYRO_XOUT_H + 2) / GYRO_SCALE
    gz = _read_word(GYRO_XOUT_H + 4) / GYRO_SCALE
    return gx, gy, gz

# ------------------------------------------------------------
# 距離測定 (HC-SR04)
SOUND_SPEED = 34300.0  # [cm/s]

def measure_distance(timeout=0.03):
    """超音波距離 [cm] (timeout 秒で失敗時 None)"""
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(10e-6)               # 10 µs パルス
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
TAP_WINDOW = 0.30        # [s] 観測窓
TAP_NEAR   = 5.0         # [cm] 近距離しきい
TAP_FAR    = 10.0        # [cm] 遠距離しきい
BLINK_TIMES = 3
BLINK_INTERVAL = 0.15    # [s]

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
            return (rng is not None
                    and self.enter_time is not None
                    and now - self.enter_time >= self.hold_sec)
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
    LOOP_DT = 0.05      # 20 Hz
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
            dist_history.appendleft(dist)          # 新しい測定を左側へ
            # エアタップ判定
            if check_air_tap():
                blink_red()
                dist_history.clear()               # 同一タップの再検出防止
            # 距離レンジ決定
            if   0.0 <= dist < 5.0:   rng = 1
            elif 5.0 <= dist < 10.0:  rng = 2
            elif 10.0 <= dist < 15.0: rng = 3
            else:                      rng = None
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
```

### 主要パラメータの調整ポイント

| 定数                    | 役割                | 既定値          | 備考                     |
| --------------------- | ----------------- | ------------ | ---------------------- |
| `GYRO_THRESHOLD`      | 各軸 LED 点灯角速度しきい値  | 150 °/s      | 手の振り方に応じて 50–300 程度で調整 |
| `RangeTimer.hold_sec` | 距離レンジ確定に必要な連続検出時間 | 1.0 s        | 誤検出を下げたい場合は長めに         |
| `TAP_WINDOW`          | エアタップ判定に使う履歴時間幅   | 0.30 s       | 手早い前後動作に合わせる           |
| `TAP_NEAR / TAP_FAR`  | エアタップ近・遠距離閾値      | 5 cm / 10 cm | 手の長さやセンサー設置位置によって調整    |
| `BLINK_TIMES`         | エアタップ時の点滅回数       | 3            | 0 にすればブリンクなし           |

---

## 4. 使い方

1. 回路を表 1 に従って配線し、`gesture_input.py` をラズパイにコピー。
2. I2C を有効化 (`raspi-config` → Interface Options → I2C → Enable)。
3. 必要パッケージをインストール（未導入の場合）

   ```bash
   sudo apt-get install -y python3-smbus python3-rpi.gpio
   ```
4. 実行

   ```bash
   python3 gesture_input.py
   ```
5. `Ctrl+C` で終了。自動で LED を消灯し GPIO を解放します。

---

## 5. カスタマイズのヒント

* **角速度レンジ切替**
  MPU6050 の GYRO\_CONFIG レジスタ（0x1B）を書き換え、感度を ±500°/s（スケール 65.5）、±1000°/s（32.8）などに変更すると、激しい動作でも飽和しにくくなります。
* **複数動作の同時検知**
  現状は単純トリガ設計ですが、ジャイロと距離を組み合わせたジェスチャ（例：手のひねり＋前後動）を追加する場合は、状態機械やイベントキューを導入して拡張してください。
* **電源管理**
  MPU6050 の加速度計やスリープモードを併用するとアイドル時の消費電流を抑えられます。

---

以上で設計と実装例を示しました。部品の特性個体差や取り付け位置により、しきい値やタイミングは調整が必要です。不明点があればお知らせください。
