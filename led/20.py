import sys

sys.path.append("..")
from mod.led import LED


def main():
    led = LED(23)
    led.on()  # LEDを点灯
    print("LEDが点灯しました。")
    input("Enterキーを押してLEDを消灯します...")
    led.off()  # LEDを消灯
    print("LEDが消灯しました。")
    input("Enterキーを押してプログラムを終了します...")


if __name__ == "__main__":
    main()
