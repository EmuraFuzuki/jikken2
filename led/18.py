import sys

sys.path.append("..")
from mod.led import LED
import time

# 使用可能なGPIOピン（4つのLED用）
USABLE_GPIOS = [2, 3, 4, 17]


def binary_counter():
    """
    4つのLEDを使って2進数で0から15までの数字を表現する
    GPIO 2: 1の位（2^0）
    GPIO 3: 2の位（2^1）
    GPIO 4: 4の位（2^2）
    GPIO 17: 8の位（2^3）
    """
    # 4つのLEDオブジェクトを作成
    leds = [LED(pin) for pin in USABLE_GPIOS]

    try:
        print("2進数カウンター開始（0-15）")
        print("Ctrl+Cで終了")

        for number in range(16):  # 0から15まで
            # 数値を2進数に変換して各LEDを制御
            binary_string = format(number, "04b")  # 4桁の2進数文字列

            print(f"数値: {number:2d}, 2進数: {binary_string}")

            # 各LEDを制御（右から左へ：1の位、2の位、4の位、8の位）
            for i, led in enumerate(leds):
                bit_value = int(binary_string[3 - i])  # 文字列を逆順で読む
                if bit_value == 1:
                    led.on()
                else:
                    led.off()

            time.sleep(1)  # 1秒間隔

        print("カウンター完了")

    except KeyboardInterrupt:
        print("\nプログラム終了")
    finally:
        # 全てのLEDを消灯
        for led in leds:
            led.off()


def manual_binary_display():
    """
    手動で数値を入力して2進数表示する
    """
    leds = [LED(pin) for pin in USABLE_GPIOS]

    try:
        print("手動2進数表示モード")
        print("0-15の数値を入力してください（qで終了）")

        while True:
            user_input = input("数値を入力: ")

            if user_input.lower() == "q":
                break

            try:
                number = int(user_input)
                if 0 <= number <= 15:
                    # 2進数表示
                    binary_string = format(number, "04b")
                    print(f"数値: {number}, 2進数: {binary_string}")

                    # LEDを制御
                    for i, led in enumerate(leds):
                        bit_value = int(binary_string[3 - i])
                        if bit_value == 1:
                            led.on()
                        else:
                            led.off()
                else:
                    print("0-15の範囲で入力してください")
            except ValueError:
                print("有効な数値を入力してください")

    except KeyboardInterrupt:
        print("\nプログラム終了")
    finally:
        # 全てのLEDを消灯
        for led in leds:
            led.off()


def main():
    print("4つのLEDによる2進数表示プログラム")
    print("1: 自動カウンター（0-15）")
    print("2: 手動入力モード")

    choice = input("選択してください (1 or 2): ")

    if choice == "1":
        binary_counter()
    elif choice == "2":
        manual_binary_display()
    else:
        print("1または2を選択してください")


if __name__ == "__main__":
    main()
