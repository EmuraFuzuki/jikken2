# 課題43: 距離計算式の検証（d = τv/2）
def main1():
    import pyvisa

    # import matplotlib.pyplot as plt
    from gpiozero import DistanceSensor
    import time
    # import os

    print("=== 課題43: 距離計算式の検証 ===")
    print("文献によると、距離 d = τv/2 (v=340 m/s)")
    print("この式がどの程度正しいか検証します")

    try:
        # 距離センサーの初期化
        sensor = DistanceSensor(echo=24, trigger=23)

        # オシロスコープとの接続
        rm = pyvisa.ResourceManager()
        visaList = rm.list_resources()
        print("接続可能な機器:")
        for vis in visaList:
            print(vis)

        if len(visaList) == 0:
            print("オシロスコープが見つかりません。センサーのみで測定を行います。")
            # センサーのみでの測定
            perform_sensor_only_measurement(sensor)
            return

        inst = rm.open_resource(visaList[0])
        print(f"接続した機器: {inst}")
        inst.timeout = 10000  # ms

        # 測定データを保存するリスト
        measurements = []

        print("\n=== 複数距離での測定 ===")
        print("異なる距離で測定を行い、計算式の精度を確認します")
        print("各測定でEnterキーを押してください（終了: q）")

        measurement_count = 0

        while True:
            try:
                user_input = input(
                    f"\n測定 {measurement_count + 1}: 実際の距離をcmで入力（終了: q）: "
                )

                if user_input.lower() == "q":
                    break

                actual_distance = float(user_input)

                print("測定中...")

                # センサーでの距離測定
                sensor_distances = []
                for i in range(5):
                    distance = sensor.distance * 100  # cm
                    sensor_distances.append(distance)
                    time.sleep(0.1)

                avg_sensor_distance = sum(sensor_distances) / len(sensor_distances)

                # オシロスコープでの波形取得
                inst.write(":SINGle")
                time.sleep(0.2)
                inst.query("*OPC?")

                # CH2（Echo信号）の設定
                inst.write(":WAVeform:SOURce CHANnel2")
                inst.write(":WAVeform:MODE NORMal")
                inst.write(":WAVeform:FORMat BYTE")

                # データ取得
                acq_record = int(inst.query("WAVeform:POINts?"))
                x_increment = float(inst.query(":WAVeform:XINCrement?"))
                x_origin = float(inst.query(":WAVeform:XORigin?"))
                x_reference = float(inst.query(":WAVeform:XREFerence?"))
                y_increment = float(inst.query(":WAVeform:YINCrement?"))
                y_origin = float(inst.query(":WAVeform:YORigin?"))
                y_reference = float(inst.query(":WAVeform:YREFerence?"))

                binwave = inst.query_binary_values(
                    ":WAVeform:DATA?",
                    datatype="B",
                    container=list,
                    chunk_size=acq_record * 1,
                )

                # データ変換
                time_data = [
                    (i - x_reference) * x_increment + x_origin
                    for i in range(len(binwave))
                ]
                voltage_data = [
                    (data - y_reference) * y_increment + y_origin for data in binwave
                ]

                # Echo信号の解析
                threshold = 0.1  # V
                echo_duration = analyze_echo_duration(
                    time_data, voltage_data, threshold
                )

                if echo_duration > 0:
                    # 距離計算（複数の音速で計算）
                    sound_speeds = [340, 343, 331]  # m/s (標準, 20℃, 0℃)
                    calculated_distances = []

                    for speed in sound_speeds:
                        distance_m = (echo_duration * speed) / 2
                        distance_cm = distance_m * 100
                        calculated_distances.append(distance_cm)

                    # 結果記録
                    measurement_data = {
                        "actual": actual_distance,
                        "sensor": avg_sensor_distance,
                        "echo_duration": echo_duration,
                        "calculated_340": calculated_distances[0],
                        "calculated_343": calculated_distances[1],
                        "calculated_331": calculated_distances[2],
                    }
                    measurements.append(measurement_data)

                    # 結果表示
                    print(f"実際の距離: {actual_distance:.1f} cm")
                    print(f"センサー測定値: {avg_sensor_distance:.1f} cm")
                    print(f"Echo持続時間: {echo_duration * 1e6:.1f} μs")
                    print("計算距離:")
                    print(f"  v=340m/s: {calculated_distances[0]:.1f} cm")
                    print(f"  v=343m/s: {calculated_distances[1]:.1f} cm")
                    print(f"  v=331m/s: {calculated_distances[2]:.1f} cm")

                    measurement_count += 1
                else:
                    print("Echo信号が検出されませんでした")

            except ValueError:
                print("数値を入力してください")
            except KeyboardInterrupt:
                print("\n測定を中断しました")
                break

        inst.write(":RUN")
        inst.close()
        rm.close()

        # 結果の解析とグラフ表示
        if len(measurements) >= 2:
            analyze_and_plot_results(measurements)
        else:
            print("解析には最低2回の測定が必要です")

    except ImportError as e:
        print(f"必要なライブラリがインストールされていません: {e}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


def analyze_echo_duration(time_data, voltage_data, threshold):
    """Echo信号の持続時間を解析"""
    high_periods = []
    in_high = False
    start_time = 0

    for i, voltage in enumerate(voltage_data):
        if voltage > threshold and not in_high:
            in_high = True
            start_time = time_data[i]
        elif voltage <= threshold and in_high:
            in_high = False
            end_time = time_data[i]
            duration = end_time - start_time
            if duration > 1e-6:  # 1μs以上のパルスのみ
                high_periods.append(duration)

    if high_periods:
        return max(high_periods)  # 最長パルスを返す
    else:
        return 0


def analyze_and_plot_results(measurements):
    """測定結果の解析とグラフ表示"""
    import matplotlib.pyplot as plt
    import os

    print("\n=== 測定結果の解析 ===")

    actual_distances = [m["actual"] for m in measurements]
    sensor_distances = [m["sensor"] for m in measurements]
    calc_340_distances = [m["calculated_340"] for m in measurements]
    calc_343_distances = [m["calculated_343"] for m in measurements]
    calc_331_distances = [m["calculated_331"] for m in measurements]

    # 誤差計算
    errors_sensor = [abs(s - a) for s, a in zip(sensor_distances, actual_distances)]
    errors_340 = [abs(c - a) for c, a in zip(calc_340_distances, actual_distances)]
    errors_343 = [abs(c - a) for c, a in zip(calc_343_distances, actual_distances)]
    errors_331 = [abs(c - a) for c, a in zip(calc_331_distances, actual_distances)]

    print(f"測定回数: {len(measurements)}")
    print(f"センサー平均誤差: {sum(errors_sensor) / len(errors_sensor):.2f} cm")
    print(f"v=340m/s 平均誤差: {sum(errors_340) / len(errors_340):.2f} cm")
    print(f"v=343m/s 平均誤差: {sum(errors_343) / len(errors_343):.2f} cm")
    print(f"v=331m/s 平均誤差: {sum(errors_331) / len(errors_331):.2f} cm")

    # 最適な音速を判定
    best_speed = min(
        [(sum(errors_340), 340), (sum(errors_343), 343), (sum(errors_331), 331)]
    )
    print(f"\n最適な音速: {best_speed[1]} m/s (総誤差: {best_speed[0]:.2f} cm)")

    # グラフ表示
    plt.figure(figsize=(15, 10))

    # 距離比較
    plt.subplot(2, 2, 1)
    plt.plot(actual_distances, actual_distances, "k--", label="理想線", alpha=0.7)
    plt.scatter(
        actual_distances, sensor_distances, color="blue", label="センサー", alpha=0.7
    )
    plt.scatter(
        actual_distances,
        calc_340_distances,
        color="red",
        label="計算(v=340m/s)",
        alpha=0.7,
    )
    plt.scatter(
        actual_distances,
        calc_343_distances,
        color="green",
        label="計算(v=343m/s)",
        alpha=0.7,
    )
    plt.scatter(
        actual_distances,
        calc_331_distances,
        color="orange",
        label="計算(v=331m/s)",
        alpha=0.7,
    )
    plt.xlabel("実際の距離 [cm]")
    plt.ylabel("測定/計算距離 [cm]")
    plt.title("距離測定精度比較")
    plt.legend()
    plt.grid(True)

    # 誤差比較
    plt.subplot(2, 2, 2)
    x_pos = range(len(measurements))
    width = 0.2
    plt.bar(
        [x - 1.5 * width for x in x_pos],
        errors_sensor,
        width,
        label="センサー",
        alpha=0.7,
    )
    plt.bar(
        [x - 0.5 * width for x in x_pos], errors_340, width, label="v=340m/s", alpha=0.7
    )
    plt.bar(
        [x + 0.5 * width for x in x_pos], errors_343, width, label="v=343m/s", alpha=0.7
    )
    plt.bar(
        [x + 1.5 * width for x in x_pos], errors_331, width, label="v=331m/s", alpha=0.7
    )
    plt.xlabel("測定回数")
    plt.ylabel("絶対誤差 [cm]")
    plt.title("測定誤差比較")
    plt.legend()
    plt.grid(True)

    # Echo時間 vs 距離
    plt.subplot(2, 2, 3)
    echo_durations = [m["echo_duration"] * 1e6 for m in measurements]  # μs
    plt.scatter(actual_distances, echo_durations, color="purple", alpha=0.7)
    # 理論線（v=340m/s）
    theoretical_times = [2 * d / 100 / 340 * 1e6 for d in actual_distances]
    plt.plot(actual_distances, theoretical_times, "r--", label="理論値(v=340m/s)")
    plt.xlabel("実際の距離 [cm]")
    plt.ylabel("Echo持続時間 [μs]")
    plt.title("Echo時間 vs 距離")
    plt.legend()
    plt.grid(True)  # 相関係数計算
    plt.subplot(2, 2, 4)
    # 各手法の相関係数を計算
    import math

    def correlation(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum([x[i] * y[i] for i in range(n)])
        sum_x2 = sum([x[i] ** 2 for i in range(n)])
        sum_y2 = sum([y[i] ** 2 for i in range(n)])

        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))

        if denominator == 0:
            return 0
        return numerator / denominator

    corr_sensor = correlation(actual_distances, sensor_distances)
    corr_340 = correlation(actual_distances, calc_340_distances)
    corr_343 = correlation(actual_distances, calc_343_distances)
    corr_331 = correlation(actual_distances, calc_331_distances)

    methods = ["センサー", "v=340m/s", "v=343m/s", "v=331m/s"]
    correlations = [corr_sensor, corr_340, corr_343, corr_331]
    avg_errors = [
        sum(errors_sensor) / len(errors_sensor),
        sum(errors_340) / len(errors_340),
        sum(errors_343) / len(errors_343),
        sum(errors_331) / len(errors_331),
    ]

    colors = ["blue", "red", "green", "orange"]
    plt.scatter(correlations, avg_errors, c=colors, s=100, alpha=0.7)
    for i, method in enumerate(methods):
        plt.annotate(
            method,
            (correlations[i], avg_errors[i]),
            xytext=(5, 5),
            textcoords="offset points",
        )
    plt.xlabel("相関係数")
    plt.ylabel("平均誤差 [cm]")
    plt.title("精度 vs 相関")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # データ保存
    data_dir = "../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filename = "../data/distance_formula_verification.txt"
    with open(filename, "w") as f:
        f.write("# Distance Formula Verification Results\n")
        f.write("# Formula: d = τv/2\n")
        f.write(f"# Number of measurements: {len(measurements)}\n")
        f.write(f"# Best sound speed: {best_speed[1]} m/s\n")
        f.write(
            "# Actual[cm]\tSensor[cm]\tEcho[μs]\tCalc340[cm]\tCalc343[cm]\tCalc331[cm]\n"
        )

        for m in measurements:
            f.write(
                f"{m['actual']:.1f}\t{m['sensor']:.1f}\t{m['echo_duration'] * 1e6:.1f}\t"
            )
            f.write(
                f"{m['calculated_340']:.1f}\t{m['calculated_343']:.1f}\t{m['calculated_331']:.1f}\n"
            )

    print(f"\n結果を {filename} に保存しました")

    print("\n=== 結論 ===")
    print("距離計算式 d = τv/2 の検証結果:")
    if best_speed[0] / len(measurements) < 1.0:
        print("✓ 式は高精度で有効（平均誤差 < 1cm）")
    elif best_speed[0] / len(measurements) < 2.0:
        print("○ 式は実用的に有効（平均誤差 < 2cm）")
    else:
        print("△ 式の精度には改善の余地あり")

    print(f"推奨音速: {best_speed[1]} m/s")
    print("注意: 温度、湿度、気圧により音速は変化します")


def perform_sensor_only_measurement(sensor):
    """センサーのみでの測定（オシロスコープなしの場合）"""
    import time

    print("\nセンサーのみでの距離測定を行います")

    measurements = []
    measurement_count = 0

    while True:
        try:
            user_input = input(
                f"\n測定 {measurement_count + 1}: 実際の距離をcmで入力（終了: q）: "
            )

            if user_input.lower() == "q":
                break

            actual_distance = float(user_input)

            # 5回測定して平均
            sensor_distances = []
            for i in range(5):
                distance = sensor.distance * 100  # cm
                sensor_distances.append(distance)
                time.sleep(0.1)

            avg_sensor_distance = sum(sensor_distances) / len(sensor_distances)
            error = abs(avg_sensor_distance - actual_distance)

            measurements.append(
                {
                    "actual": actual_distance,
                    "sensor": avg_sensor_distance,
                    "error": error,
                }
            )

            print(f"実際の距離: {actual_distance:.1f} cm")
            print(f"センサー測定値: {avg_sensor_distance:.1f} cm")
            print(f"誤差: {error:.1f} cm")

            measurement_count += 1

        except ValueError:
            print("数値を入力してください")
        except KeyboardInterrupt:
            print("\n測定を中断しました")
            break

    if measurements:
        avg_error = sum([m["error"] for m in measurements]) / len(measurements)
        print(f"\n平均誤差: {avg_error:.2f} cm")
        print("センサー内部で距離計算式が使用されていると推定されます")
