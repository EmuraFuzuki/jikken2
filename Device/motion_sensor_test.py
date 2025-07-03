import RPi.GPIO as GPIO
import time


def main1():
    # GPIOピンの指定
    SENSOR_PIN = 17  # センサーのOUTピンを接続したGPIOピン番号

    # GPIOの初期設定
    GPIO.setmode(GPIO.BCM)  # GPIO番号でピンを指定するモード
    GPIO.setup(SENSOR_PIN, GPIO.IN)  # SENSOR_PINを入力モードに設定

    print("PIR Module Test (Ctrl+C to exit)")
    time.sleep(2)  # センサーの初期化待ち
    print("Ready")

    try:
        while True:
            # センサーの状態を読み込む
            sensor_state = GPIO.input(SENSOR_PIN)
            if sensor_state == 1:
                print("Motion Detected!")
            else:
                print("................")

            time.sleep(0.1)  # 0.1秒待機

    except KeyboardInterrupt:
        print(" Quit")

    finally:
        GPIO.cleanup()  # GPIO設定をクリーンアップ
