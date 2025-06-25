# 課題38: T字拡張ボードとGPIOケーブルでの接続確認とLED点灯回路
def main1():
    print("=== 課題38: T字拡張ボードとGPIOケーブルでの接続確認 ===")
    print("この課題では以下を確認します:")
    print("1. T字拡張ボードと40pinGPIOケーブル（リボンケーブル）の接続")
    print("2. 以前行ったLED点灯回路が動作することの確認")
    print()

    try:
        from gpiozero import LED
        from time import sleep

        # GPIO13番ピンにLEDを接続
        led = LED(13)

        print("LED点灯テストを開始します...")
        print("3回点滅させます。LEDが点滅すれば接続成功です。")
        print("点滅しない場合は以下を確認してください:")
        print("- GPIOケーブルが正しく接続されているか")
        print("- T字拡張ボードの向きが正しいか")
        print("- LEDの極性が正しいか（長い脚がプラス側）")
        print("- 抵抗が正しく接続されているか")
        print()

        for i in range(3):
            print(f"点滅 {i + 1}/3")
            led.on()
            print("LED ON")
            sleep(1)
            led.off()
            print("LED OFF")
            sleep(1)

        print("\nLED点滅テスト完了")
        print("LEDが正常に点滅した場合、接続は成功です！")

    except ImportError:
        print("gpiozeroライブラリがインストールされていません")
        print("以下のコマンドでインストールしてください:")
        print("pip install gpiozero")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("接続を確認してください:")
        print("1. GPIOケーブルの接続方向")
        print("2. T字拡張ボードの向き")
        print("3. LED回路の配線")

    print("\n=== 接続確認のポイント ===")
    print("1. Raspberry Piの電源を切った状態で配線する")
    print("2. GPIOケーブルの1番ピン（通常赤い線）がRaspberry Piの1番ピンに対応")
    print("3. T字拡張ボードの番号とRaspberry Piのピン番号が一致")
    print("4. LEDの向きに注意（アノード=長い脚をプラス側に）")
    print("5. 適切な抵抗値を使用（220Ω～1kΩ程度）")
