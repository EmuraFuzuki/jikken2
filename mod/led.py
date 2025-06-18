import gpiozero
import time
import math
import threading


class LED:
    """
    PWMLEDをベースに、デジタル点灯（オン／オフ）、点滅、モールス信号送信
    フェードイン／アウト、呼吸効果、パルス効果など
    多彩なエフェクトを提供する統合LEDクラス。

    Attributes:
        device (gpiozero.PWMLED): PWM出力対応LEDデバイス
        interval (float): toggle_led用の点滅間隔（秒）
        time_length (float): toggle_led用の継続時間（秒）
        _blink_thread (threading.Thread): start_blink用スレッド
        _blinking (bool): start_blink用フラグ

    Methods:
        on(): 完全点灯
        off(): 消灯
        toggle(): 現在状態を反転
        toggle_led(time_length=None, interval=None):
            デジタル点滅（先のクラスの機能をそのまま残し）
        show_interval(): toggle_ledの設定を表示
        blink(on_time=0.5, off_time=0.5, n=None):
            同期的に点滅
        start_blink(on_time=0.5, off_time=0.5):
            非同期点滅開始
        stop_blink(): 非同期点滅停止
        strobe(rate=10, duration=3.0): 高速ストロボ点滅
        pattern(sequence): 任意の点灯/消灯パターン
        morse(message, unit=0.2): モールス信号送信
        fade_in(duration=2.0, steps=100): フェードイン
        fade_out(duration=2.0, steps=100): フェードアウト
        breathing_effect(duration=10.0, cycle_time=3.0): 呼吸効果
        pulse_effect(duration=8.0, pulse_width=1.0): パルス効果
        set_brightness(brightness): PWMで直接明るさ制御
        turn_off(): PWMLEDを消灯
    """

    MORSE_CODE = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
    }

    def __init__(self, pin, interval=1.0, time_length=3.0, frequency=1000):
        self.device = gpiozero.PWMLED(pin, frequency=frequency)
        self.interval = interval
        self.time_length = time_length
        self._blink_thread = None
        self._blinking = False

    # ── デジタル点灯制御 ─────────────────────────────────────────────

    def on(self):
        """LEDを完全点灯"""
        self._stop_blinking()
        self.device.on()

    def off(self):
        """LEDを消灯"""
        self._stop_blinking()
        self.device.off()

    def toggle(self):
        """現在のオン／オフ状態を反転"""
        self._stop_blinking()
        if self.device.value > 0:
            self.device.off()
        else:
            self.device.on()

    def toggle_led(self, time_length=None, interval=None):
        """
        指定間隔で点滅（先のクラスのまま）
        Args:
            time_length (float): 継続時間（秒）
            interval (float): 点滅間隔（秒）
        """
        if time_length is not None:
            self.time_length = time_length
        if interval is not None:
            self.interval = interval
        self.show_interval()
        end_time = time.time() + self.time_length
        while time.time() < end_time:
            self.device.on()
            time.sleep(self.interval)
            self.device.off()
            time.sleep(self.interval)

    def show_interval(self):
        """toggle_ledの設定（間隔と周波数、継続時間）を表示"""
        freq = 1 / (2 * self.interval)
        print(
            f"LED点滅: 間隔 {self.interval:.3f}秒, 周波数 {freq:.1f}Hz, 継続 {self.time_length:.1f}秒"
        )

    def blink(self, on_time=0.5, off_time=0.5, n=None):
        """
        同期的に点滅
        Args:
            on_time (float): 点灯時間
            off_time (float): 消灯時間
            n (int or None): 回数(Noneで無限)
        """
        self._stop_blinking()
        count = 0
        while n is None or count < n:
            self.device.on()
            time.sleep(on_time)
            self.device.off()
            time.sleep(off_time)
            count += 1

    def start_blink(self, on_time=0.5, off_time=0.5):
        """
        非同期点滅開始（バックグラウンド）
        停止は stop_blink() で
        """
        if self._blinking:
            return
        self._blinking = True

        def _worker():
            while self._blinking:
                self.device.on()
                time.sleep(on_time)
                if not self._blinking:
                    break
                self.device.off()
                time.sleep(off_time)

        self._blink_thread = threading.Thread(target=_worker, daemon=True)
        self._blink_thread.start()

    def stop_blink(self):
        """非同期点滅停止＆消灯"""
        self._stop_blinking()
        self.device.off()

    def strobe(self, rate=10, duration=3.0):
        """
        ブロッキングの高速ストロボ点滅
        Args:
            rate (float): 1秒あたりの点滅回数
            duration (float): 継続時間
        """
        self._stop_blinking()
        interval = 1.0 / rate / 2
        end_time = time.time() + duration
        while time.time() < end_time:
            self.device.on()
            time.sleep(interval)
            self.device.off()
            time.sleep(interval)

    def pattern(self, sequence):
        """
        任意の点灯/消灯パターン
        Args:
            sequence (list of tuple(bool, float)):
                (True=点灯/False=消灯, 継続時間)
        """
        self._stop_blinking()
        for state, dur in sequence:
            if state:
                self.device.on()
            else:
                self.device.off()
            time.sleep(dur)

    def morse(self, message, unit=0.2):
        """
        英数字メッセージをモールス信号で送信
        Args:
            message (str): 英数字と空白
            unit (float): 基本単位時間
        """
        self._stop_blinking()
        for word in message.upper().split(" "):
            for ch in word:
                code = self.MORSE_CODE.get(ch)
                if not code:
                    continue
                for sym in code:
                    self.device.on()
                    time.sleep(unit if sym == "." else 3 * unit)
                    self.device.off()
                    time.sleep(unit)
                time.sleep(2 * unit)
            time.sleep(4 * unit)

    # ── PWM制御機能 ────────────────────────────────────────────────────

    def fade_in(self, duration=2.0, steps=100):
        """フェードイン"""
        self._stop_blinking()
        step_t = duration / steps
        for i in range(steps + 1):
            self.device.value = i / steps
            time.sleep(step_t)

    def fade_out(self, duration=2.0, steps=100):
        """フェードアウト"""
        self._stop_blinking()
        step_t = duration / steps
        for i in range(steps + 1):
            self.device.value = 1 - (i / steps)
            time.sleep(step_t)

    def breathing_effect(self, duration=10.0, cycle_time=3.0):
        """呼吸効果（サイン波）"""
        self._stop_blinking()
        start = time.time()
        while time.time() - start < duration:
            t = time.time() - start
            self.device.value = (math.sin(2 * math.pi * t / cycle_time) + 1) / 2
            time.sleep(0.05)

    def pulse_effect(self, duration=8.0, pulse_width=1.0):
        """パルス効果"""
        self._stop_blinking()
        start = time.time()
        while time.time() - start < duration:
            self.fade_in(duration=pulse_width * 0.2, steps=20)
            self.fade_out(duration=pulse_width * 0.8, steps=40)
            time.sleep(0.5)

    def set_brightness(self, brightness):
        """明るさを直接設定（0.0〜1.0）"""
        self._stop_blinking()
        b = max(0.0, min(1.0, brightness))
        self.device.value = b

    def turn_off(self):
        """LEDを消灯（PWM版）"""
        self._stop_blinking()
        self.device.off()

    # ── 内部ユーティリティ ─────────────────────────────────────────────

    def _stop_blinking(self):
        """非同期点滅を安全に停止"""
        if self._blinking:
            self._blinking = False
            if self._blink_thread:
                self._blink_thread.join()
            self._blink_thread = None

    def close(self):
        """GPIOリソース解放"""
        self._stop_blinking()
        self.device.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
