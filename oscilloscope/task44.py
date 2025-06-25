# 課題44: 周期的に10μsのパルスを発生するプログラム
def main1():
    print("=== 課題44: 10μsパルス生成プログラム ===")

    try:
        from gpiozero import DigitalOutputDevice
        import time

        # GPIO23をTrigger信号用に設定
        trigger = DigitalOutputDevice(23)

        print("10μsのパルスを周期的に発生させます")
        print("オシロスコープでGPIO23の信号を観察してください")
        print("停止するにはCtrl+Cを押してください")
        print()
        print("=== オシロスコープ設定推奨 ===")
        print("- 時間軸: 20μs/div")
        print("- 電圧軸: 1V/div")
        print("- トリガー: CH1の立ち上がりエッジ")
        print("- トリガーレベル: 1.5V")
        print()

        input("準備ができたらEnterキーを押してください...")

        pulse_count = 0
        start_time = time.time()

        try:
            while True:
                # 10μsのパルスを生成
                trigger.on()  # High
                time.sleep(10e-6)  # 10マイクロ秒待機
                trigger.off()  # Low

                pulse_count += 1

                # 100ms間隔でパルスを生成（観察しやすくするため）
                time.sleep(0.1)

                # 1秒ごとに状況を表示
                if pulse_count % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"パルス生成数: {pulse_count}, 経過時間: {elapsed:.1f}秒")

        except KeyboardInterrupt:
            trigger.off()  # 安全のためOFFにする
            elapsed = time.time() - start_time
            print("\nパルス生成を停止しました")
            print(f"総パルス数: {pulse_count}")
            print(f"総経過時間: {elapsed:.1f}秒")
            print(
                f"パルス周期: {elapsed / pulse_count * 1000:.1f}ms"
                if pulse_count > 0
                else ""
            )

        print("\n=== 観察すべきポイント ===")
        print("1. パルス幅:")
        print("   - 約10μsの正のパルス")
        print("   - 立ち上がり/立ち下がり時間の確認")
        print()
        print("2. パルス振幅:")
        print("   - 3.3V（Raspberry PiのGPIO電圧）")
        print("   - HighとLowのレベルの確認")
        print()
        print("3. パルス周期:")
        print("   - 約100ms間隔（観察用に設定）")
        print("   - 実際の距離センサーでは測定に応じて変化")
        print()
        print("4. 波形品質:")
        print("   - オーバーシュート/アンダーシュートの有無")
        print("   - ノイズレベルの確認")

        # パルス幅の精度テスト
        print("\n=== パルス幅精度テスト ===")
        print("異なるパルス幅での動作確認")

        test_widths = [5e-6, 10e-6, 20e-6, 50e-6]  # 5μs, 10μs, 20μs, 50μs

        for width in test_widths:
            print(f"\nパルス幅 {width * 1e6:.0f}μs でテスト中...")
            for i in range(5):
                trigger.on()
                time.sleep(width)
                trigger.off()
                time.sleep(0.1)  # 観察用の間隔
                print(".", end="", flush=True)
            print(" 完了")

        trigger.off()  # 最終的にOFFにする

        print("\n=== 考察 ===")
        print("1. Pythonでの時間制御の限界:")
        print("   - time.sleep()の精度はOS依存")
        print("   - μs単位の制御では誤差が生じる可能性")
        print("   - より高精度にはハードウェアタイマーが必要")
        print()
        print("2. 実際の距離センサーでの使用:")
        print("   - HC-SR04は10μs以上のパルスが必要")
        print("   - パルス幅が短すぎると動作しない")
        print("   - 長すぎても問題なし（ただし無駄な消費電力）")

    except ImportError:
        print("gpiozeroライブラリがインストールされていません")
        print("pip install gpiozero")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("GPIO設定を確認してください")
