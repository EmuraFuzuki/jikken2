import gpiozero
import time
import threading


class LED:
    """
    LEDクラスは、指定されたGPIOピンでLEDを制御します。
    点灯、消灯、点滅、ストロボ、パターン点灯、モールス信号送信などの機能を提供します。

    Attributes:
        pin (int): GPIOピン番号
        device (gpiozero.DigitalOutputDevice): LED制御デバイス
        _blink_thread (threading.Thread): 非同期点滅用スレッド
        _blinking (bool): 点滅中フラグ
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

    def __init__(self, pin):
        self.pin = pin
        self.device = gpiozero.DigitalOutputDevice(pin)
        self._blink_thread = None
        self._blinking = False

    def on(self):
        """LEDを点灯する"""
        self._stop_blinking()
        self.device.on()

    def off(self):
        """LEDを消灯する"""
        self._stop_blinking()
        self.device.off()

    def toggle(self):
        """LEDの現在状態を反転する"""
        self._stop_blinking()
        if self.device.value:
            self.device.off()
        else:
            self.device.on()

    def blink(self, on_time=0.5, off_time=0.5, n=None):
        """
        LEDを指定した時間で点滅させる（ブロッキングモード）。
        Args:
            on_time (float): 点灯時間（秒）
            off_time (float): 消灯時間（秒）
            n (int or None): 点滅回数。Noneなら無限に繰り返す。
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
        LEDを非同期に点滅させ始める（バックグラウンドスレッド）。
        停止するには stop_blink() を呼び出す。
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
        """非同期点滅を停止し、LEDを消灯する"""
        self._stop_blinking()
        self.device.off()

    def strobe(self, rate=10, duration=3.0):
        """
        高速点滅（ストロボ）を行う（ブロッキングモード）。
        Args:
            rate (float): 1秒あたりの点滅回数
            duration (float): 実行時間（秒）
        """
        interval = 1.0 / rate / 2
        end_time = time.time() + duration
        while time.time() < end_time:
            self.device.on()
            time.sleep(interval)
            self.device.off()
            time.sleep(interval)

    def pattern(self, sequence):
        """
        任意の点灯・消灯パターンを実行する。
        Args:
            sequence (list of tuple(bool, float)):
                (状態, 継続時間秒) のリスト。
                Trueなら点灯、Falseなら消灯を sequence の順に行う。
        """
        self._stop_blinking()
        for state, duration in sequence:
            if state:
                self.device.on()
            else:
                self.device.off()
            time.sleep(duration)

    def morse(self, message, unit=0.2):
        """
        英数字メッセージをモールス信号で送信する（ブロッキングモード）。
        Args:
            message (str): 送信する文字列（英数字と空白のみ）
            unit (float): モールス信号の基本単位時間（秒）
        """
        self._stop_blinking()
        for word in message.upper().split(" "):
            for char in word:
                code = self.MORSE_CODE.get(char)
                if not code:
                    continue
                for symbol in code:
                    self.device.on()
                    time.sleep(unit if symbol == "." else 3 * unit)
                    self.device.off()
                    time.sleep(unit)
                # 文字間隔
                time.sleep(2 * unit)
            # 単語間隔
            time.sleep(4 * unit)

    def _stop_blinking(self):
        """内部：非同期点滅を安全に停止する"""
        if self._blinking:
            self._blinking = False
            if self._blink_thread:
                self._blink_thread.join()
            self._blink_thread = None

    def close(self):
        """GPIOリソースを解放する"""
        self._stop_blinking()
        self.device.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
