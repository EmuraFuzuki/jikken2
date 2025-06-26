# 課題41: オシロスコープとの通信でEcho端子の波形を記録
def main1():
    import pyvisa
    import matplotlib.pyplot as plt
    from gpiozero import DistanceSensor
    import time
    import japanize_matplotlib

    print("=== 課題41: オシロスコープとの通信でEcho波形記録 ===")

    try:
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
        result = inst.query("*IDN?")
        print(f"機器ID: {result}")
        inst.timeout = 10000  # ms

        # 距離センサーの初期化
        sensor = DistanceSensor(echo=24, trigger=23)

        print("\n=== 測定手順 ===")
        print("1. オシロスコープのCH2をGPIO24(Echo)に接続")
        print("2. プローブのGNDをブレッドボードのGNDに接続")
        print("3. オシロスコープの設定:")
        print("   - CH2をアクティブに設定")
        print("   - 時間軸と電圧軸を適切に設定してください")
        print("   - 推奨設定: 時間軸 100μs/div、電圧軸 1V/div")
        print("   - トリガー: AUTO または NORMAL")
        print("   - Echo信号が見えるように調整してください")

        # オシロスコープの現在設定を取得・表示
        print("\n=== 現在のオシロスコープ設定 ===")
        try:
            # CH2の時間軸設定を取得
            time_scale = float(inst.query(":TIMebase:SCALe?"))
            print(f"時間軸: {time_scale * 1e6:.1f} μs/div")

            # CH2の電圧軸設定を取得
            volt_scale = float(inst.query(":CHANnel2:SCALe?"))
            print(f"CH2電圧軸: {volt_scale:.3f} V/div")

            # オフセット設定を取得
            volt_offset = float(inst.query(":CHANnel2:OFFSet?"))
            print(f"CH2オフセット: {volt_offset:.3f} V")

        except Exception as e:
            print(f"設定取得エラー: {e}")
            print("手動で設定を確認してください")

        input("\n設定確認・調整完了後、Enterキーを押してください...")

        # 距離測定を1回実行してトリガー
        print("距離測定を実行中...")
        distance = sensor.distance * 1000  # mm
        print(f"測定距離: {distance:.1f} mm")

        # 少し待機してからオシロスコープで波形を取得
        time.sleep(0.5)

        # シングルショット測定に設定
        inst.write(":SINGle")
        time.sleep(0.1)
        inst.query("*OPC?")

        # CH2の波形を取得できるように設定
        inst.write(":WAVeform:SOURce CHANnel2")
        inst.write(":WAVeform:MODE NORMal")
        inst.write(":WAVeform:FORMat BYTE")

        # データ点数を取得
        acq_record = int(inst.query("WAVeform:POINts?"))
        print(f"データ点数: {acq_record}")

        # 軸のスケール情報を取得
        x_increment = float(inst.query(":WAVeform:XINCrement?"))
        x_origin = float(inst.query(":WAVeform:XORigin?"))
        x_reference = float(inst.query(":WAVeform:XREFerence?"))

        y_increment = float(inst.query(":WAVeform:YINCrement?"))
        y_origin = float(inst.query(":WAVeform:YORigin?"))
        y_reference = float(inst.query(":WAVeform:YREFerence?"))

        print(f"時間分解能: {x_increment * 1e6:.2f} μs/point")

        # 波形データを取得
        binwave = inst.query_binary_values(
            ":WAVeform:DATA?", datatype="B", container=list, chunk_size=acq_record * 1
        )

        # 自動測定に変更
        inst.write(":RUN")
        inst.close()
        rm.close()

        # 時間軸とデータをスケールに変換
        time_data = [
            (i - x_reference) * x_increment + x_origin for i in range(len(binwave))
        ]
        voltage_data = [
            (data - y_reference) * y_increment + y_origin for data in binwave
        ]

        # Echo信号の解析
        print("\n=== Echo信号の解析 ===")

        # 自動で適切な閾値を設定
        # 電圧データの最大値と最小値から閾値を計算
        max_voltage = max(voltage_data)
        min_voltage = min(voltage_data)
        threshold = (
            min_voltage + (max_voltage - min_voltage) * 0.5
        )  # 中間値を閾値とする

        print(f"検出された電圧範囲: {min_voltage:.3f}V ～ {max_voltage:.3f}V")
        print(f"自動設定閾値: {threshold:.3f}V")

        # Echo信号のHighの期間を検出
        high_periods = []
        in_high = False
        start_time = 0

        for i, voltage in enumerate(voltage_data):
            if voltage > threshold and not in_high:
                # Highの開始
                in_high = True
                start_time = time_data[i]
            elif voltage <= threshold and in_high:
                # Highの終了
                in_high = False
                end_time = time_data[i]
                duration = end_time - start_time
                high_periods.append((start_time, end_time, duration))

        # 最も長いHighパルスを見つける（Echo信号と推定）
        if high_periods:
            echo_pulse = max(high_periods, key=lambda x: x[2])
            echo_duration = echo_pulse[2]
            echo_start = echo_pulse[0]
            echo_end = echo_pulse[1]

            # 距離計算
            sound_speed = 340  # m/s
            calculated_distance = (echo_duration * sound_speed) / 2 * 100  # cm

            print(f"Echo信号開始時刻: {echo_start * 1e6:.1f} μs")
            print(f"Echo信号終了時刻: {echo_end * 1e6:.1f} μs")
            print(f"Echo信号持続時間: {echo_duration * 1e6:.1f} μs")
            print(f"計算距離: {calculated_distance:.1f} cm")
            print(f"センサー測定値: {distance / 10:.1f} cm")
            print(f"誤差: {abs(calculated_distance - distance / 10):.1f} cm")
        else:
            print("Echo信号が検出されませんでした")
            echo_duration = 0

        # グラフ表示
        plt.figure(figsize=(12, 8))

        # 全体の波形
        plt.subplot(2, 1, 1)
        plt.plot([t * 1e6 for t in time_data], voltage_data, "b-", linewidth=1)
        plt.axhline(
            y=threshold,
            color="r",
            linestyle="--",
            alpha=0.7,
            label=f"閾値 {threshold:.3f}V",
        )
        if high_periods:
            for start, end, dur in high_periods:
                plt.axvspan(start * 1e6, end * 1e6, alpha=0.3, color="yellow")
        plt.xlabel("Time [μs]")
        plt.ylabel("Voltage [V]")
        plt.title("Echo Signal Waveform (Full)")
        plt.legend()
        plt.grid(True)

        # Echo信号部分の拡大
        if high_periods and echo_duration > 0:
            plt.subplot(2, 1, 2)
            # Echo信号周辺のデータを抽出
            start_idx = max(0, int((echo_start - x_origin) / x_increment) - 100)
            end_idx = min(
                len(time_data), int((echo_end - x_origin) / x_increment) + 100
            )

            zoom_time = time_data[start_idx:end_idx]
            zoom_voltage = voltage_data[start_idx:end_idx]

            plt.plot([t * 1e6 for t in zoom_time], zoom_voltage, "b-", linewidth=2)
            plt.axhline(
                y=threshold,
                color="r",
                linestyle="--",
                alpha=0.7,
                label=f"閾値 {threshold:.3f}V",
            )
            plt.axvspan(
                echo_start * 1e6,
                echo_end * 1e6,
                alpha=0.3,
                color="yellow",
                label=f"Echo ({echo_duration * 1e6:.1f}μs)",
            )
            plt.xlabel("Time [μs]")
            plt.ylabel("Voltage [V]")
            plt.title("Echo Signal Waveform (Zoomed)")
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.show()

        # データ保存
        import os

        data_dir = "../data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        filename = "../data/echo_signal.txt"
        with open(filename, "w") as f:
            f.write("# Echo Signal Data\n")
            f.write(f"# Measured Distance: {distance:.1f} mm\n")
            f.write(f"# Echo Duration: {echo_duration * 1e6:.1f} μs\n")
            f.write(f"# Calculated Distance: {calculated_distance:.1f} cm\n")
            f.write("# Time[μs]\tVoltage[V]\n")
            for t, v in zip(time_data, voltage_data):
                f.write(f"{t * 1e6:.3f}\t{v:.6f}\n")

        print(f"\nデータを {filename} に保存しました")

    except ImportError as e:
        print(f"必要なライブラリがインストールされていません: {e}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("接続を確認してください")
