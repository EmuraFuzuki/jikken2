import sys
sys.path.append('..')
from mod.led import LED
import time

# 使用可能なGPIOピン
USABLE_GPIOS = [2, 3, 4, 17]


def test_independent_leds():
    """
    4つの赤いLEDを独立に操作できることを確認するテスト関数
    """
    print("4つのLEDを独立に操作するテストを開始します...")

    # 4つのLEDオブジェクトを作成
    leds = []
    for pin in USABLE_GPIOS:
        led = LED(pin)
        leds.append(led)
        print(f"LED on GPIO {pin} initialized")

    print("\n=== テスト1: 全てのLEDを順番に点灯/消灯 ===")
    for i, led in enumerate(leds):
        print(f"LED {i + 1} (GPIO {USABLE_GPIOS[i]}) を点灯")
        led.on()
        time.sleep(1)
        print(f"LED {i + 1} (GPIO {USABLE_GPIOS[i]}) を消灯")
        led.off()
        time.sleep(0.5)

    print("\n=== テスト2: 全てのLEDを同時に点灯 ===")
    for i, led in enumerate(leds):
        led.on()
        print(f"LED {i + 1} (GPIO {USABLE_GPIOS[i]}) 点灯")
    time.sleep(2)

    print("\n=== テスト3: 全てのLEDを同時に消灯 ===")
    for i, led in enumerate(leds):
        led.off()
        print(f"LED {i + 1} (GPIO {USABLE_GPIOS[i]}) 消灯")
    time.sleep(1)

    print("\n=== テスト4: LEDを1つずつ点灯（他は消灯のまま） ===")
    for i, led in enumerate(leds):
        # 全て消灯
        for other_led in leds:
            other_led.off()
        # 1つだけ点灯
        led.on()
        print(f"LED {i + 1} (GPIO {USABLE_GPIOS[i]}) のみ点灯中...")
        time.sleep(1.5)

    print("\n=== テスト5: 点滅パターンテスト ===")
    # LED1とLED3を点灯、LED2とLED4を消灯
    print("LED1,3を点灯、LED2,4を消灯")
    leds[0].on()  # LED1
    leds[1].off()  # LED2
    leds[2].on()  # LED3
    leds[3].off()  # LED4
    time.sleep(2)

    # パターンを反転
    print("LED1,3を消灯、LED2,4を点灯")
    leds[0].off()  # LED1
    leds[1].on()  # LED2
    leds[2].off()  # LED3
    leds[3].on()  # LED4
    time.sleep(2)

    print("\n=== テスト6: 順次点灯（流れるパターン） ===")
    for cycle in range(3):  # 3回繰り返し
        print(f"サイクル {cycle + 1}")
        for i in range(len(leds)):
            # 全て消灯
            for led in leds:
                led.off()
            # 1つだけ点灯
            leds[i].on()
            time.sleep(0.3)

    # 最後に全て消灯
    print("\n=== テスト完了: 全LEDを消灯 ===")
    for i, led in enumerate(leds):
        led.off()
        print(f"LED {i + 1} (GPIO {USABLE_GPIOS[i]}) 消灯")

    print("\nテスト完了！4つのLEDが独立に操作できることを確認しました。")


def test_individual_control():
    """
    個別のLED制御をユーザーが手動で確認できる関数
    """
    print("個別LED制御テストモード")
    print("各LEDを個別に操作して独立性を確認します")

    # LEDオブジェクト作成
    leds = [LED(pin) for pin in USABLE_GPIOS]

    print("\n利用可能なコマンド:")
    print("on <番号>  : 指定したLEDを点灯 (例: on 1)")
    print("off <番号> : 指定したLEDを消灯 (例: off 2)")
    print("toggle <番号> : 指定したLEDの状態を反転 (例: toggle 3)")
    print("all_on     : 全LEDを点灯")
    print("all_off    : 全LEDを消灯")
    print("quit       : 終了")
    print(f"\nLED番号: 1-4 (GPIO {USABLE_GPIOS})")

    while True:
        try:
            command = input("\nコマンドを入力: ").strip().lower()

            if command == "quit":
                break
            elif command == "all_on":
                for i, led in enumerate(leds):
                    led.on()
                    print(f"LED {i + 1} 点灯")
            elif command == "all_off":
                for i, led in enumerate(leds):
                    led.off()
                    print(f"LED {i + 1} 消灯")
            elif command.startswith(("on ", "off ", "toggle ")):
                parts = command.split()
                if len(parts) == 2:
                    action = parts[0]
                    try:
                        led_num = int(parts[1])
                        if 1 <= led_num <= 4:
                            led_index = led_num - 1
                            if action == "on":
                                leds[led_index].on()
                                print(
                                    f"LED {led_num} (GPIO {USABLE_GPIOS[led_index]}) 点灯"
                                )
                            elif action == "off":
                                leds[led_index].off()
                                print(
                                    f"LED {led_num} (GPIO {USABLE_GPIOS[led_index]}) 消灯"
                                )
                            elif action == "toggle":
                                leds[led_index].toggle()
                                status = (
                                    "点灯"
                                    if leds[led_index].device.value > 0
                                    else "消灯"
                                )
                                print(
                                    f"LED {led_num} (GPIO {USABLE_GPIOS[led_index]}) {status}"
                                )
                        else:
                            print("LED番号は1-4で指定してください")
                    except ValueError:
                        print("正しい番号を入力してください")
                else:
                    print("コマンド形式が正しくありません")
            else:
                print("無効なコマンドです")

        except KeyboardInterrupt:
            break

    # 終了時に全LEDを消灯
    print("\n終了中... 全LEDを消灯します")
    for led in leds:
        led.off()
    print("テスト終了")


if __name__ == "__main__":
    print("LEDテストプログラム")
    print("1: 自動テスト実行")
    print("2: 手動制御テスト")

    try:
        choice = input("選択してください (1 or 2): ").strip()

        if choice == "1":
            test_independent_leds()
        elif choice == "2":
            test_individual_control()
        else:
            print("1または2を選択してください")

    except KeyboardInterrupt:
        print("\nプログラムを終了します")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
