# 課題40: 距離センサーのTrigとEcho信号をオシロスコープで観察
def main1():
    print("=== 課題40: 距離センサーのTrig/Echo信号のオシロスコープ観察 ===")

    try:
        from gpiozero import DistanceSensor
        from time import sleep

        # HC-SR04距離センサー（Echo=24, Trigger=23）
        sensor = DistanceSensor(echo=24, trigger=23)

        print("距離センサーのTrig/Echo信号をオシロスコープで観察します")
        print()
        print("=== 配線指示 ===")
        print("オシロスコープのプローブを以下のように接続してください:")
        print("- CH1: GPIO 23 (Trig信号)")
        print("- CH2: GPIO 24 (Echo信号)")
        print("- プローブのGND: ブレッドボードのGNDライン")
        print()
        print("=== オシロスコープの設定推奨 ===")
        print("- 時間軸: 50μs/div 程度")
        print("- 電圧軸: 1V/div")
        print("- トリガー: CH1 (Trig信号) の立ち上がりエッジ")
        print("- トリガーレベル: 1.5V")
        print()

        input("配線とオシロスコープの設定が完了したらEnterキーを押してください...")

        print("距離測定を開始します。オシロスコープで波形を確認してください。")
        print("測定を停止するにはCtrl+Cを押してください。")
        print()

        try:
            measurement_count = 0
            while True:
                distance = sensor.distance * 1000  # mm
                measurement_count += 1
                print(f"測定 {measurement_count}: 距離 = {distance:.1f} mm")
                sleep(1)

        except KeyboardInterrupt:
            print(f"\n測定を停止しました（{measurement_count}回測定）")

        print("\n=== 観察すべき波形の特徴 ===")
        print("1. Trig信号:")
        print("   - 約10μsの正のパルス")
        print("   - 3.3Vの振幅")
        print("   - 測定開始のトリガー")
        print()
        print("2. Echo信号:")
        print("   - Trig信号の後に遅れて発生")
        print("   - パルス幅が距離に比例")
        print("   - 3.3Vの振幅")
        print("   - 超音波の往復時間を表す")
        print()
        print("3. 関係式:")
        print("   - 距離 = (Echo信号の幅 × 音速) / 2")
        print("   - 音速 ≈ 340 m/s")
        print("   - 例: Echo幅が1000μsの場合")
        print("     距離 = (1000×10⁻⁶ × 340) / 2 = 0.17 m = 17 cm")
        print()
        print("4. 測定可能な距離範囲:")
        print("   - 最小: 約2cm（超音波の指向性による）")
        print("   - 最大: 約400cm（HC-SR04の仕様）")
        print("   - 精度: ±3mm（理想的な条件下）")

    except ImportError:
        print("gpiozeroライブラリがインストールされていません")
        print("pip install gpiozero")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("センサーの接続を確認してください")
