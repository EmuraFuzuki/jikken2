

# LED クラス

PWM制御とデジタル制御を統合した、多彩な点灯エフェクトを提供する Python クラスです。  
GPIO Zero の `PWMLED` を用いて、明るさ制御（フェード、呼吸、パルスなど）とデジタル点灯（オン／オフ、点滅、モールス信号など）を同一インスタンスで扱えます。

---

## 目次

- [LED クラス](#led-クラス)
  - [目次](#目次)
  - [前提条件](#前提条件)
  - [インストール](#インストール)
  - [クラス概要](#クラス概要)
  - [使用例](#使用例)
  - [メソッド一覧](#メソッド一覧)
    - [デジタル制御](#デジタル制御)
    - [PWM 制御](#pwm-制御)
    - [その他](#その他)
  - [注意点](#注意点)

---

## 前提条件

- Raspberry Pi 等の GPIO 出力が可能な環境  
- Python 3.x  
- `gpiozero` ライブラリ  

---

## インストール

```
pip install gpiozero
```

---

## クラス概要

`LED` クラスは、GPIO ピンを用いて LED の制御を行います。

```python
led = LED(pin=17, interval=0.5, time_length=5.0, frequency=500)
```

* `pin`: GPIO ピン番号
* `interval`: `toggle_led` の点滅間隔（秒）
* `time_length`: `toggle_led` の継続時間（秒）
* `frequency`: PWM の周波数（Hz）

LED デバイスには `PWMLED` を用いており、`on()/off()` によるフル点灯・消灯や、`device.value = x` で 0.0〜1.0 の間の明るさ制御が可能です。

---

## 使用例

```python
import time
from led import LED

led = LED(pin=17)

# 1. 単純点灯・消灯
led.on()
time.sleep(1)
led.off()

# 2. デジタル点滅（toggle_led）
led.toggle_led(time_length=4.0, interval=0.3)

# 3. 同期的点滅
led.blink(on_time=0.2, off_time=0.2, n=10)

# 4. 非同期点滅
led.start_blink(on_time=0.1, off_time=0.1)
time.sleep(3)
led.stop_blink()

# 5. モールス信号で“HELLO”
led.morse("HELLO", unit=0.15)

# 6. フェードイン／アウト
led.fade_in(duration=2.0, steps=50)
led.fade_out(duration=2.0, steps=50)

# 7. 呼吸効果
led.breathing_effect(duration=8.0, cycle_time=2.0)

# 8. パルス効果
led.pulse_effect(duration=5.0, pulse_width=0.8)

# 9. 明るさ設定
led.set_brightness(0.6)
time.sleep(1)
led.turn_off()

# 終了時に GPIO を解放
led.close()
```

---

## メソッド一覧

### デジタル制御

* `on()` / `off()` / `toggle()`
* `toggle_led(time_length=None, interval=None)`
* `show_interval()`
* `blink(on_time, off_time, n=None)`
* `start_blink(on_time, off_time)` / `stop_blink()`
* `strobe(rate, duration)`
* `pattern(sequence)`
* `morse(message, unit)`

### PWM 制御

* `fade_in(duration, steps)`
* `fade_out(duration, steps)`
* `breathing_effect(duration, cycle_time)`
* `pulse_effect(duration, pulse_width)`
* `set_brightness(brightness)`
* `turn_off()`

### その他

* `close()` / コンテキストマネージャ対応

---

## 注意点

* 非同期点滅中は他の同期的エフェクト呼び出しで自動的に停止されます。
* モールス信号実行中はブロッキングします。必要に応じてスレッドで呼び出してください。
* PWMLED を用いているため、明るさ制御が不要ならば `device.on()/off()` で従来のデジタルLEDにも対応します。
