# 課題47: gpiozeroを使わずに距離を取得するプログラム
def main1():
    print("=== 課題47: gpiozeroを使わない距離測定プログラム ===")

    try:
        from gpiozero import DigitalOutputDevice, DigitalInputDevice
        import time

        # GPIO設定
        trigger_pin = 23
        echo_pin = 24

        # ピンの初期化
        trigger = DigitalOutputDevice(trigger_pin)
        echo = DigitalInputDevice(echo_pin)

        print("HC-SR04超音波距離センサーを手動制御で距離測定します")
        print(f"Trigger Pin: GPIO{trigger_pin}")
        print(f"Echo Pin: GPIO{echo_pin}")
        print()

        def measure_distance():
            """距離を測定する関数"""

            # 1. トリガーパルスの生成（10μs以上のパルス）
            trigger.off()  # 確実にLowにする
            time.sleep(0.000002)  # 2μs待機

            trigger.on()  # High
            time.sleep(0.00001)  # 10μs待機
            trigger.off()  # Low

            # 2. Echo信号の立ち上がりを待つ（タイムアウト付き）
            timeout_start = time.perf_counter()
            timeout_duration = 0.1  # 100ms タイムアウト

            while not echo.is_active:
                if time.perf_counter() - timeout_start > timeout_duration:
                    print("タイムアウト: Echo信号の立ち上がりが検出されませんでした")
                    return None
                time.sleep(0.000001)  # 1μs待機

            # 3. Echo信号の立ち上がり時刻を記録
            start_time = time.perf_counter()

            # 4. Echo信号の立ち下がりを待つ
            timeout_start = time.perf_counter()

            while echo.is_active:
                if time.perf_counter() - timeout_start > timeout_duration:
                    print("タイムアウト: Echo信号の立ち下がりが検出されませんでした")
                    return None
                time.sleep(0.000001)  # 1μs待機

            # 5. Echo信号の立ち下がり時刻を記録
            end_time = time.perf_counter()

            # 6. 持続時間の計算
            pulse_duration = end_time - start_time

            # 7. 距離の計算 (d = τv/2, v = 340 m/s)
            sound_speed = 340  # m/s
            distance = (pulse_duration * sound_speed) / 2

            return distance, pulse_duration

        print("距離測定を開始します...")
        print("測定を停止するにはCtrl+Cを押してください")
        print()

        measurement_count = 0
        successful_measurements = []

        try:
            while True:
                measurement_count += 1
                print(f"測定 {measurement_count}: ", end="", flush=True)

                result = measure_distance()

                if result is not None:
                    distance, pulse_duration = result
                    distance_cm = distance * 100  # mをcmに変換

                    # 妥当性チェック（HC-SR04の仕様範囲）
                    if 0.02 <= distance <= 4.0:  # 2cm～400cm
                        successful_measurements.append(
                            {
                                "distance_cm": distance_cm,
                                "pulse_duration_us": pulse_duration * 1e6,
                                "measurement_num": measurement_count,
                            }
                        )

                        print(
                            f"距離 = {distance_cm:.1f} cm, "
                            f"Echo時間 = {pulse_duration * 1e6:.1f} μs"
                        )
                    else:
                        print(f"範囲外の値: {distance_cm:.1f} cm (無視)")
                else:
                    print("測定失敗")

                time.sleep(0.5)  # 0.5秒間隔で測定

        except KeyboardInterrupt:
            print(f"\n測定を停止しました。総測定回数: {measurement_count}")

        # 測定結果の統計
        if successful_measurements:
            distances = [m["distance_cm"] for m in successful_measurements]
            pulse_times = [m["pulse_duration_us"] for m in successful_measurements]
            print("\n=== 測定結果統計 ===")
            print(f"成功した測定: {len(successful_measurements)}/{measurement_count}")
            print(
                f"成功率: {len(successful_measurements) / measurement_count * 100:.1f}%"
            )
            print(f"平均距離: {sum(distances) / len(distances):.1f} cm")
            print(f"最小距離: {min(distances):.1f} cm")
            print(f"最大距離: {max(distances):.1f} cm")
            print(f"平均Echo時間: {sum(pulse_times) / len(pulse_times):.1f} μs")

            # 測定精度の評価
            if len(distances) > 1:
                # 標準偏差の計算
                mean_distance = sum(distances) / len(distances)
                variance = sum([(d - mean_distance) ** 2 for d in distances]) / len(
                    distances
                )
                std_dev = variance**0.5

                print(f"距離の標準偏差: {std_dev:.2f} cm")
                print(f"変動係数: {std_dev / mean_distance * 100:.1f}%")

        print("\n=== 改良版: エラーハンドリング強化 ===")

        def measure_distance_robust():
            """エラーハンドリングを強化した距離測定関数"""

            max_retries = 3

            for attempt in range(max_retries):
                try:
                    # センサーを安定させるための待機
                    time.sleep(0.01)

                    # トリガーパルス生成
                    trigger.off()
                    time.sleep(0.000002)
                    trigger.on()
                    time.sleep(0.00001)
                    trigger.off()

                    # Echo信号の監視（より短いタイムアウト）
                    timeout = 0.05  # 50ms

                    # 立ち上がり待ち
                    start_wait = time.perf_counter()
                    while not echo.is_active:
                        if time.perf_counter() - start_wait > timeout:
                            raise TimeoutError("Echo立ち上がりタイムアウト")
                        time.sleep(0.0000005)  # 0.5μs

                    pulse_start = time.perf_counter()

                    # 立ち下がり待ち
                    start_wait = time.perf_counter()
                    while echo.is_active:
                        if time.perf_counter() - start_wait > timeout:
                            raise TimeoutError("Echo立ち下がりタイムアウト")
                        time.sleep(0.0000005)  # 0.5μs

                    pulse_end = time.perf_counter()

                    pulse_duration = pulse_end - pulse_start

                    # 妥当性チェック
                    if pulse_duration < 0.000116:  # 2cm未満（音速340m/sで約116μs）
                        raise ValueError("パルス時間が短すぎます")

                    if pulse_duration > 0.023:  # 400cm超（約23ms）
                        raise ValueError("パルス時間が長すぎます")

                    # 距離計算
                    distance = (pulse_duration * 340) / 2 * 100  # cm

                    return distance, pulse_duration, attempt + 1

                except (TimeoutError, ValueError) as e:
                    if attempt == max_retries - 1:
                        return None, str(e), attempt + 1
                    time.sleep(0.01)  # リトライ前の待機

            return None, "最大リトライ回数に到達", max_retries

        print("改良版での測定を行います（10回）...")

        for i in range(10):
            print(f"測定 {i + 1:2d}: ", end="", flush=True)

            result = measure_distance_robust()

            if result[0] is not None:
                distance, pulse_duration, attempts = result
                print(f"{distance:.1f} cm (試行{attempts}回目で成功)")
            else:
                error_msg, attempts = result[1], result[2]
                print(f"失敗 - {error_msg} (試行{attempts}回)")

            time.sleep(0.3)

        print("\n=== gpiozeroのDistanceSensorとの比較 ===")

        # gpiozeroでの測定も実行
        from gpiozero import DistanceSensor

        sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

        print("同じセンサーをgpiozeroのDistanceSensorでも測定...")

        gpiozero_distances = []
        manual_distances = []

        for i in range(5):
            # 手動測定
            manual_result = measure_distance_robust()

            # gpiozero測定
            gpiozero_distance = sensor.distance * 100  # cm

            print(f"測定 {i + 1}:")

            if manual_result[0] is not None:
                manual_distance = manual_result[0]
                manual_distances.append(manual_distance)
                print(f"  手動実装: {manual_distance:.1f} cm")
            else:
                print("  手動実装: 測定失敗")

            gpiozero_distances.append(gpiozero_distance)
            print(f"  gpiozero: {gpiozero_distance:.1f} cm")

            if manual_result[0] is not None:
                diff = abs(manual_distance - gpiozero_distance)
                print(f"  差: {diff:.1f} cm")

            time.sleep(0.5)

        if manual_distances and gpiozero_distances:
            manual_avg = sum(manual_distances) / len(manual_distances)
            gpiozero_avg = sum(gpiozero_distances) / len(gpiozero_distances)

            print("\n平均値比較:")
            print(f"手動実装: {manual_avg:.1f} cm")
            print(f"gpiozero: {gpiozero_avg:.1f} cm")
            print(f"平均差: {abs(manual_avg - gpiozero_avg):.1f} cm")

        print("\n=== まとめ ===")
        print("1. 手動実装の利点:")
        print("   - 動作原理の理解")
        print("   - 細かい制御が可能")
        print("   - デバッグ情報の取得")
        print()
        print("2. gpiozeroライブラリの利点:")
        print("   - 実装が簡単")
        print("   - エラーハンドリングが組み込み済み")
        print("   - 安定した動作")
        print()
        print("3. 学習効果:")
        print("   - タイミング制御の重要性")
        print("   - ハードウェア制御の基本")
        print("   - エラーハンドリングの必要性")

    except ImportError:
        print("gpiozeroライブラリがインストールされていません")
        print("pip install gpiozero")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("センサーの接続を確認してください")
