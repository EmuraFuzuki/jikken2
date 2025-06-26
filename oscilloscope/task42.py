# 課題42: 波形データを解析してEcho出力のHigh持続時間を求める
def main1():
    import pyvisa
    import matplotlib.pyplot as plt

    print("=== 課題42: Echo信号のHigh持続時間解析 ===")

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

        print("\n距離センサーを動作させてからオシロスコープで波形を取得します")
        input("準備ができたらEnterキーを押してください...")

        # HC-SR04距離センサー（Echo=24, Trigger=23）
        sensor = DistanceSensor(echo=24, trigger=23)

        # timeモジュールをインポート
        import time

        # オシロスコープの設定
        print("オシロスコープを設定中...")
        inst.write(":CHANnel2:DISPlay ON")  # CH2を表示
        inst.write(":CHANnel2:SCALe 1")  # CH2の縦軸スケールを1V/div
        inst.write(":CHANnel2:OFFSet 0")  # CH2のオフセットを0V
        inst.write(":TIMebase:SCALe 0.0001")  # 時間軸を100μs/div
        inst.write(":TRIGger:SOURce CHANnel2")  # CH2をトリガーソースに
        inst.write(":TRIGger:LEVel 0.1")  # トリガーレベルを0.1V（HC-SR04は3.3V信号）
        inst.write(":TRIGger:SLOPe POSitive")  # 正エッジトリガー

        # トリガーモードをNORMALに設定
        inst.write(":TRIGger:SWEep NORMal")

        print("測定準備完了")

        # 連続測定とシングルショットを組み合わせた方法
        max_attempts = 5
        acq_record = 0

        for attempt in range(max_attempts):
            print(f"\n=== 測定試行 {attempt + 1}/{max_attempts} ===")

            # シングルショット測定に設定
            inst.write(":SINGle")
            time.sleep(0.1)

            print("距離センサーの測定を開始します...")

            # センサーの測定を実行（これによりTrigger信号とEcho信号が生成される）
            try:
                distance = sensor.distance
                print(f"測定距離: {distance:.3f} m ({distance * 100:.1f} cm)")

                # 測定後少し待機
                time.sleep(0.2)

            except Exception as e:
                print(f"センサー測定中にエラー: {e}")
                continue

            # トリガー状態確認
            try:
                trig_status = inst.query(":TRIGger:STATus?").strip()
                print(f"トリガー状態: {trig_status}")
            except Exception:
                print("トリガー状態確認不可")

            # CH2（Echo信号）の波形を取得
            inst.write(":WAVeform:SOURce CHANnel2")
            inst.write(":WAVeform:MODE NORMal")
            inst.write(":WAVeform:FORMat BYTE")

            # データ点数を取得
            try:
                acq_record = int(inst.query("WAVeform:POINts?"))
                print(f"データ点数: {acq_record}")

                if acq_record > 100:  # 十分なデータが取得できた場合
                    print("波形データの取得に成功しました")
                    break
                else:
                    print("データ点数が少なすぎます。再試行...")
                    # 連続測定に戻して再度トリガーを待つ
                    inst.write(":RUN")
                    time.sleep(0.5)

            except Exception as e:
                print(f"データ点数取得エラー: {e}")
                inst.write(":RUN")
                time.sleep(0.5)

        if acq_record <= 0:
            print("\n波形データの取得に失敗しました")
            print("確認事項:")
            print("- CH2にEcho信号（GPIO24）が正しく接続されているか")
            print("- トリガーレベルが適切か（Echo信号レベルより低く設定）")
            print("- センサーが正常に動作しているか")
            inst.write(":RUN")
            inst.close()
            rm.close()
            return

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
            inst.write(":RUN")
            inst.close()
            rm.close()
            return

        # 波形データを取得
        try:
            binwave = inst.query_binary_values(
                ":WAVeform:DATA?", datatype="B", container=list, chunk_size=acq_record
            )
            print(f"取得した生データ点数: {len(binwave)}")

            if len(binwave) == 0:
                print("波形データが空です")
                inst.write(":RUN")
                inst.close()
                rm.close()
                return

        except Exception as e:
            print(f"波形データ取得エラー: {e}")
            inst.write(":RUN")
            inst.close()
            rm.close()
            return

        # 自動測定に変更
        inst.write(":RUN")
        inst.close()
        rm.close()

        # 時間軸とデータをスケールに変換
        try:
            time_data = [
                (i - x_reference) * x_increment + x_origin for i in range(len(binwave))
            ]
            voltage_data = [
                (data - y_reference) * y_increment + y_origin for data in binwave
            ]

            print(f"総測定時間: {(time_data[-1] - time_data[0]) * 1e3:.2f} ms")
            print(f"電圧範囲: {min(voltage_data):.3f}V ～ {max(voltage_data):.3f}V")

        except Exception as e:
            print(f"データ変換エラー: {e}")
            return

        # Echo信号のHigh持続時間を解析
        print("\n=== Echo信号のHigh持続時間解析 ===")

        def analyze_echo_signal(time_data, voltage_data):
            """Echo信号のHigh持続時間を解析する"""

            # 複数の閾値で解析を行う
            thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            results = []

            for threshold in thresholds:
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

                results.append({"threshold": threshold, "periods": high_periods})

            return results

        # 解析実行
        analysis_results = analyze_echo_signal(time_data, voltage_data)

        # 結果表示
        for result in analysis_results:
            threshold = result["threshold"]
            periods = result["periods"]

            print(f"\n閾値 {threshold:.1f}V での解析結果:")
            print(f"  検出されたHighパルス数: {len(periods)}")

            if periods:
                # 最も長いパルス（Echo信号と推定）
                longest_pulse = max(periods, key=lambda x: x["duration"])
                echo_duration = longest_pulse["duration"]

                print(f"  最長パルス持続時間: {echo_duration * 1e6:.1f} μs")
                print(f"  開始時刻: {longest_pulse['start_time'] * 1e6:.1f} μs")
                print(f"  終了時刻: {longest_pulse['end_time'] * 1e6:.1f} μs")

                # 距離計算
                sound_speed = 340  # m/s
                calculated_distance = (echo_duration * sound_speed) / 2 * 100  # cm
                print(f"  計算距離: {calculated_distance:.2f} cm")

                # 全パルスの情報
                if len(periods) > 1:
                    print("  全パルス情報:")
                    for i, period in enumerate(periods):
                        print(f"    パルス{i + 1}: {period['duration'] * 1e6:.1f} μs")

        # 最適な閾値を選択（最も安定した結果を得る）
        optimal_result = None
        for result in analysis_results:
            if len(result["periods"]) >= 1:
                optimal_result = result
                break

        if optimal_result:
            echo_pulse = max(optimal_result["periods"], key=lambda x: x["duration"])
            optimal_threshold = optimal_result["threshold"]

            print(f"\n=== 最終結果（閾値 {optimal_threshold:.1f}V） ===")
            print(f"Echo信号持続時間 τ: {echo_pulse['duration'] * 1e6:.2f} μs")

            # グラフ表示
            plt.figure(figsize=(14, 10))

            # 全波形表示
            plt.subplot(3, 1, 1)
            plt.plot([t * 1e6 for t in time_data], voltage_data, "b-", linewidth=1)
            plt.axhline(
                y=optimal_threshold,
                color="r",
                linestyle="--",
                alpha=0.7,
                label=f"閾値 {optimal_threshold:.1f}V",
            )
            for period in optimal_result["periods"]:
                plt.axvspan(
                    period["start_time"] * 1e6,
                    period["end_time"] * 1e6,
                    alpha=0.3,
                    color="yellow",
                )
            plt.xlabel("Time [μs]")
            plt.ylabel("Voltage [V]")
            plt.title("Echo Signal Analysis - Full Waveform")
            plt.legend()
            plt.grid(True)

            # Echo信号部分の拡大
            plt.subplot(3, 1, 2)
            margin = 50  # データポイント
            start_idx = max(0, echo_pulse["start_idx"] - margin)
            end_idx = min(len(time_data), echo_pulse["end_idx"] + margin)

            zoom_time = time_data[start_idx:end_idx]
            zoom_voltage = voltage_data[start_idx:end_idx]

            plt.plot([t * 1e6 for t in zoom_time], zoom_voltage, "b-", linewidth=2)
            plt.axhline(y=optimal_threshold, color="r", linestyle="--", alpha=0.7)
            plt.axvspan(
                echo_pulse["start_time"] * 1e6,
                echo_pulse["end_time"] * 1e6,
                alpha=0.3,
                color="yellow",
                label=f"Echo pulse: {echo_pulse['duration'] * 1e6:.1f}μs",
            )
            plt.axvline(
                x=echo_pulse["start_time"] * 1e6, color="g", linestyle=":", alpha=0.8
            )
            plt.axvline(
                x=echo_pulse["end_time"] * 1e6, color="g", linestyle=":", alpha=0.8
            )
            plt.xlabel("Time [μs]")
            plt.ylabel("Voltage [V]")
            plt.title("Echo Signal Analysis - Zoomed View")
            plt.legend()
            plt.grid(True)

            # 複数閾値での比較
            plt.subplot(3, 1, 3)
            durations_by_threshold = []
            threshold_values = []

            for result in analysis_results:
                if result["periods"]:
                    longest = max(result["periods"], key=lambda x: x["duration"])
                    durations_by_threshold.append(longest["duration"] * 1e6)
                    threshold_values.append(result["threshold"])

            if durations_by_threshold:
                plt.plot(
                    threshold_values,
                    durations_by_threshold,
                    "o-",
                    linewidth=2,
                    markersize=8,
                )
                plt.xlabel("Threshold [V]")
                plt.ylabel("Echo Duration [μs]")
                plt.title("Echo Duration vs Threshold")
                plt.grid(True)

            plt.tight_layout()
            plt.show()

            # データ保存
            import os

            data_dir = "../data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            filename = "../data/echo_analysis.txt"
            with open(filename, "w") as f:
                f.write("# Echo Signal Analysis Results\n")
                f.write(f"# Optimal Threshold: {optimal_threshold:.1f} V\n")
                f.write(f"# Echo Duration: {echo_pulse['duration'] * 1e6:.2f} μs\n")
                f.write(f"# Start Time: {echo_pulse['start_time'] * 1e6:.1f} μs\n")
                f.write(f"# End Time: {echo_pulse['end_time'] * 1e6:.1f} μs\n")
                f.write("# Time[μs]\tVoltage[V]\n")
                for t, v in zip(time_data, voltage_data):
                    f.write(f"{t * 1e6:.3f}\t{v:.6f}\n")

            print(f"\n解析結果を {filename} に保存しました")

        else:
            print("\nEcho信号が検出されませんでした")
            print("確認事項:")
            print("- センサーが正常に動作しているか")
            print("- オシロスコープのプローブが正しく接続されているか")
            print("- 測定範囲内に障害物があるか")

    except ImportError as e:
        print(f"必要なライブラリがインストールされていません: {e}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("接続を確認してください")


if __name__ == "__main__":
    # メイン関数を実行
    main1()

    # デバッグモードを実行する場合
    # main_debug()
