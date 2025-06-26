# 課題42: 異なる距離での測定により距離計算式の精度を検証する
def main1():
    import pyvisa
    import matplotlib.pyplot as plt
    import time

    print("=== 課題42: 距離計算式の精度検証 ===")
    print("d = τv/2 (v = 340 m/s) の精度を異なる距離で検証します")

    try:
        from gpiozero import DistanceSensor

        # オシロスコープとの接続
        rm = pyvisa.ResourceManager()
        visaList = rm.list_resources()
        print("接続可能な機器:")
        for vis in visaList:
            print(vis)

        if len(visaList) == 0:
            print("オシロスコープが見つかりません")
            return

        inst = rm.open_resource(visaList[0])
        print(f"接続した機器: {inst}")
        inst.timeout = 10000  # ms

        # HC-SR04距離センサー（Echo=24, Trigger=23）
        sensor = DistanceSensor(echo=24, trigger=23)

        # 結果を保存するリスト
        measurement_results = []

        while True:
            print("\n" + "=" * 50)
            print("新しい測定を開始します")
            print("物体を適切な位置に配置してください")

            # 実際の距離を入力
            try:
                actual_distance = float(input("実際の距離 [cm]: "))
            except ValueError:
                print("数値を入力してください")
                continue
            except KeyboardInterrupt:
                print("\n測定を終了します")
                break

            input("準備ができたらEnterキーを押してください...")

            # シングルショット測定
            inst.write(":SINGle")
            time.sleep(0.1)

            print("距離センサーの測定を開始します...")

            # センサーの測定を実行
            try:
                sensor_distance = sensor.distance
                print(
                    f"センサー測定距離: {sensor_distance:.3f} m ({sensor_distance * 100:.1f} cm)"
                )
                time.sleep(0.2)
            except Exception as e:
                print(f"センサー測定中にエラー: {e}")
                continue

            # 波形データを取得
            inst.write(":WAVeform:SOURce CHANnel2")
            inst.write(":WAVeform:MODE NORMal")
            inst.write(":WAVeform:FORMat BYTE")

            # データ点数を取得
            try:
                acq_record = int(inst.query("WAVeform:POINts?"))
                print(f"データ点数: {acq_record}")

                if acq_record <= 100:
                    print("データ点数が不足しています。再試行してください。")
                    continue

            except Exception as e:
                print(f"データ点数取得エラー: {e}")
                continue

            # 軸のスケール情報を取得
            try:
                x_increment = float(inst.query(":WAVeform:XINCrement?"))
                x_origin = float(inst.query(":WAVeform:XORigin?"))
                x_reference = float(inst.query(":WAVeform:XREFerence?"))

                y_increment = float(inst.query(":WAVeform:YINCrement?"))
                y_origin = float(inst.query(":WAVeform:YORigin?"))
                y_reference = float(inst.query(":WAVeform:YREFerence?"))

                print(f"時間分解能: {x_increment * 1e6:.2f} μs/point")

            except Exception as e:
                print(f"スケール情報取得エラー: {e}")
                continue

            # 波形データを取得
            try:
                binwave = inst.query_binary_values(
                    ":WAVeform:DATA?",
                    datatype="B",
                    container=list,
                    chunk_size=acq_record,
                )
                print(f"取得した生データ点数: {len(binwave)}")

                if len(binwave) == 0:
                    print("波形データが空です")
                    continue

            except Exception as e:
                print(f"波形データ取得エラー: {e}")
                continue

            # 時間軸とデータをスケールに変換
            try:
                time_data = [
                    (i - x_reference) * x_increment + x_origin
                    for i in range(len(binwave))
                ]
                voltage_data = [
                    (data - y_reference) * y_increment + y_origin for data in binwave
                ]

                print(f"総測定時間: {(time_data[-1] - time_data[0]) * 1e3:.2f} ms")
                print(f"電圧範囲: {min(voltage_data):.3f}V ～ {max(voltage_data):.3f}V")

            except Exception as e:
                print(f"データ変換エラー: {e}")
                continue

            # Echo信号のHigh持続時間を解析（閾値0.1V固定）
            print("\n=== Echo信号解析（閾値: 0.1V） ===")

            threshold = 0.1
            high_periods = []
            in_high = False
            start_time = 0
            start_idx = 0

            for i, voltage in enumerate(voltage_data):
                if voltage > threshold and not in_high:
                    # Highの開始
                    in_high = True
                    start_time = time_data[i]
                    start_idx = i
                elif voltage <= threshold and in_high:
                    # Highの終了
                    in_high = False
                    end_time = time_data[i]
                    duration = end_time - start_time

                    # 最小パルス幅フィルタ（1μs以上）
                    if duration > 1e-6:
                        high_periods.append(
                            {
                                "start_time": start_time,
                                "end_time": end_time,
                                "duration": duration,
                                "start_idx": start_idx,
                                "end_idx": i,
                            }
                        )

            if not high_periods:
                print("Echo信号が検出されませんでした")
                continue

            # 最も長いパルス（Echo信号と推定）
            echo_pulse = max(high_periods, key=lambda x: x["duration"])
            echo_duration = echo_pulse["duration"]

            print(f"検出されたHighパルス数: {len(high_periods)}")
            print(f"Echo信号持続時間 τ: {echo_duration * 1e6:.2f} μs")
            print(f"開始時刻: {echo_pulse['start_time'] * 1e6:.1f} μs")
            print(f"終了時刻: {echo_pulse['end_time'] * 1e6:.1f} μs")

            # 距離計算
            sound_speed = 340  # m/s
            calculated_distance = (echo_duration * sound_speed) / 2 * 100  # cm
            print(f"計算距離: {calculated_distance:.2f} cm")
            print(f"実測距離: {actual_distance:.1f} cm")

            # 誤差計算
            error = abs(calculated_distance - actual_distance)
            error_percent = (error / actual_distance) * 100
            print(f"誤差: {error:.2f} cm ({error_percent:.1f}%)")

            # グラフ表示
            plt.figure(figsize=(12, 8))

            # 波形表示
            plt.subplot(2, 1, 1)
            plt.plot([t * 1e6 for t in time_data], voltage_data, "b-", linewidth=1)
            plt.axhline(
                y=threshold,
                color="r",
                linestyle="--",
                alpha=0.7,
                label=f"閾値 {threshold:.1f}V",
            )
            plt.axvspan(
                echo_pulse["start_time"] * 1e6,
                echo_pulse["end_time"] * 1e6,
                alpha=0.3,
                color="yellow",
                label=f"Echo pulse: {echo_duration * 1e6:.1f}μs",
            )
            plt.xlabel("Time [μs]")
            plt.ylabel("Voltage [V]")
            plt.title(f"Echo Signal (距離: {actual_distance:.1f}cm)")
            plt.legend()
            plt.grid(True)

            # Echo信号部分の拡大表示
            plt.subplot(2, 1, 2)
            margin = 50
            start_idx = max(0, echo_pulse["start_idx"] - margin)
            end_idx = min(len(time_data), echo_pulse["end_idx"] + margin)

            zoom_time = time_data[start_idx:end_idx]
            zoom_voltage = voltage_data[start_idx:end_idx]

            plt.plot([t * 1e6 for t in zoom_time], zoom_voltage, "b-", linewidth=2)
            plt.axhline(y=threshold, color="r", linestyle="--", alpha=0.7)
            plt.axvspan(
                echo_pulse["start_time"] * 1e6,
                echo_pulse["end_time"] * 1e6,
                alpha=0.3,
                color="yellow",
            )
            plt.xlabel("Time [μs]")
            plt.ylabel("Voltage [V]")
            plt.title("Echo Signal - 拡大表示")
            plt.grid(True)

            plt.tight_layout()
            plt.show()

            # 継続するかどうかを確認
            continue_choice = input("\n別の距離で測定を続けますか？ (y/n): ").lower()
            if continue_choice != "y":
                break

        # 測定終了後の結果まとめ
        if measurement_results:
            print("\n" + "=" * 60)
            print("=== 測定結果のまとめ ===")
            print("実測距離[cm]\t計算距離[cm]\tEcho時間[μs]\t誤差[cm]\t誤差[%]")
            print("-" * 60)

            for result in measurement_results:
                print(
                    f"{result['actual_distance']:8.1f}\t"
                    f"{result['calculated_distance']:8.2f}\t"
                    f"{result['echo_duration']:8.2f}\t"
                    f"{result['error']:6.2f}\t"
                    f"{result['error_percent']:6.1f}"
                )

            # 結果をファイルに保存
            import os

            data_dir = "../data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            filename = "../data/distance_verification.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("# 距離計算式 d = τv/2 (v = 340 m/s) の精度検証結果\n")
                f.write(
                    "# 実測距離[cm]\t計算距離[cm]\tEcho時間[μs]\t誤差[cm]\t誤差[%]\n"
                )
                for result in measurement_results:
                    f.write(
                        f"{result['actual_distance']:.1f}\t"
                        f"{result['calculated_distance']:.2f}\t"
                        f"{result['echo_duration']:.2f}\t"
                        f"{result['error']:.2f}\t"
                        f"{result['error_percent']:.1f}\n"
                    )

            print(f"\n結果を {filename} に保存しました")

            # 統計情報
            errors = [r["error"] for r in measurement_results]
            error_percents = [r["error_percent"] for r in measurement_results]

            print("\n=== 統計情報 ===")
            print(f"測定回数: {len(measurement_results)}")
            print(f"平均誤差: {sum(errors) / len(errors):.2f} cm")
            print(f"最大誤差: {max(errors):.2f} cm")
            print(f"最小誤差: {min(errors):.2f} cm")
            print(f"平均誤差率: {sum(error_percents) / len(error_percents):.1f}%")

        # オシロスコープの接続を閉じる
        inst.close()
        rm.close()
        print("\nオシロスコープとの接続を終了しました")

    except ImportError as e:
        print(f"必要なライブラリがインストールされていません: {e}")
        print("gpiozero と pyvisa をインストールしてください")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("接続を確認してください")


if __name__ == "__main__":
    # メイン関数を実行
    main1()
