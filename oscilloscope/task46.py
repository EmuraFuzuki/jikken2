# 課題46: タクトスイッチの長押し時間測定プログラム
def main1():
    print("=== 課題46: タクトスイッチの長押し時間測定 ===")

    try:
        from gpiozero import Button
        import time

        # GPIO2番ピンにタクトスイッチを接続（プルアップ抵抗使用）
        button = Button(22)

        print("タクトスイッチの長押し時間を測定します")
        print()
        print("=== 回路構成 ===")
        print("- タクトスイッチの一端: GPIO22")
        print("- タクトスイッチの他端: GND")
        print("- 内蔵プルアップ抵抗を使用")
        print()
        print("=== 使用方法 ===")
        print("- ボタンを押してから離すまでの時間を測定")
        print("- 複数回測定可能")
        print("- 終了するにはCtrl+Cを押す")
        print()

        input("回路の準備ができたらEnterキーを押してください...")

        measurement_count = 0

        try:
            while True:
                print(f"\n--- 測定 {measurement_count + 1} ---")
                print("ボタンを押してください...")

                # ボタンが押されるまで待機
                button.wait_for_press()
                start_time = time.perf_counter()
                print("ボタンが押されました。離すまでの時間を測定中...")

                # ボタンが離されるまで待機
                button.wait_for_release()
                end_time = time.perf_counter()

                press_duration = end_time - start_time
                measurement_count += 1

                print(
                    f"押下時間: {press_duration:.3f}秒 ({press_duration * 1000:.1f}ms)"
                )

                # 分類
                if press_duration < 0.1:
                    print("→ 短押し")
                elif press_duration < 1.0:
                    print("→ 中押し")
                elif press_duration < 3.0:
                    print("→ 長押し")
                else:
                    print("→ 超長押し")

                print("次の測定の準備中... （少し待ってからボタンを押してください）")
                time.sleep(0.5)  # デバウンス対策

        except KeyboardInterrupt:
            print(f"\n測定を終了しました。総測定回数: {measurement_count}")

        print("\n=== 別のアプローチ（ポーリング方式）===")
        print("連続的にボタンの状態をチェックする方法でも実装してみます")

        input("Enterキーを押すとポーリング方式でのテストを開始します...")

        print("ボタンを押してください（ポーリング方式）...")
        measurement_count_polling = 0

        try:
            while (
                measurement_count_polling < 3
            ):  # 3回のみテスト                # ボタンがLowである限り時刻を取得し、start_timeに時刻を代入し続ける
                while not button.is_pressed:
                    start_time = time.perf_counter()
                    time.sleep(0.001)  # 1ms間隔でチェック

                print("ボタンが押されました（ポーリング検出）")

                # ボタンがHighである限り時刻を取得し、end_timeに時刻を代入し続ける
                while button.is_pressed:
                    end_time = time.perf_counter()
                    time.sleep(0.001)  # 1ms間隔でチェック

                press_duration = end_time - start_time
                measurement_count_polling += 1

                print(f"押下時間（ポーリング）: {press_duration:.3f}秒")
                print("次の測定まで2秒待機...")
                time.sleep(2)

                if measurement_count_polling < 3:
                    print(
                        f"ボタンを押してください（{measurement_count_polling + 1}/3回目）..."
                    )

        except KeyboardInterrupt:
            print("ポーリング方式のテストを中断しました")

        print("\n=== イベント駆動方式の実装 ===")
        print("コールバック関数を使用した高精度測定")

        # グローバル変数（関数間でデータを共有）
        press_start_time = None
        press_durations = []

        def button_pressed():
            """ボタンが押された時のコールバック関数"""
            nonlocal press_start_time
            press_start_time = time.perf_counter()
            print("ボタン押下開始（イベント検出）")

        def button_released():
            """ボタンが離された時のコールバック関数"""
            nonlocal press_start_time, press_durations
            if press_start_time is not None:
                release_time = time.perf_counter()
                duration = release_time - press_start_time
                press_durations.append(duration)
                print(f"ボタン押下終了: {duration:.3f}秒")
                press_start_time = None

        # イベントハンドラーを設定
        button.when_pressed = button_pressed
        button.when_released = button_released

        print("イベント駆動方式での測定を開始します（10秒間）")
        print("ボタンを何度か押してください...")

        start_test_time = time.time()
        try:
            while time.time() - start_test_time < 10:
                time.sleep(0.1)  # メインループ

            print("\nイベント駆動方式での測定結果:")
            print(f"総測定回数: {len(press_durations)}")
            if press_durations:
                avg_duration = sum(press_durations) / len(press_durations)
                min_duration = min(press_durations)
                max_duration = max(press_durations)
                print(f"平均押下時間: {avg_duration:.3f}秒")
                print(f"最短押下時間: {min_duration:.3f}秒")
                print(f"最長押下時間: {max_duration:.3f}秒")

                print("\n全測定結果:")
                for i, duration in enumerate(press_durations):
                    print(f"  {i + 1:2d}: {duration:.3f}秒")

        except KeyboardInterrupt:
            print("イベント駆動方式のテストを中断しました")

        # イベントハンドラーをクリア
        button.when_pressed = None
        button.when_released = None

        print("\n=== 3つの方式の比較 ===")
        print("1. wait_for_press/release方式:")
        print("   - 簡単に実装できる")
        print("   - ブロッキング動作")
        print("   - 他の処理と並行できない")
        print()
        print("2. ポーリング方式:")
        print("   - 状態を連続的にチェック")
        print("   - CPU使用率が高い")
        print("   - チェック間隔により精度が決まる")
        print()
        print("3. イベント駆動方式:")
        print("   - 最も高精度")
        print("   - CPU効率が良い")
        print("   - 他の処理と並行可能")
        print("   - 複雑な処理に適している")

    except ImportError:
        print("gpiozeroライブラリがインストールされていません")
        print("pip install gpiozero")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("タクトスイッチの配線を確認してください")
        print("- GPIO2とGNDの間にタクトスイッチを接続")
        print("- 内蔵プルアップ抵抗が有効になっているか確認")
