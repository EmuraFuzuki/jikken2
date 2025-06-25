# 課題35: 信号発生器の設定を変更して動作確認
def main1():
    import pyvisa
    import numpy as np
    import time

    rm = pyvisa.ResourceManager()
    visaList = rm.list_resources()
    print("接続可能な機器:")
    for vis in visaList:
        print(vis)

    if len(visaList) > 0:
        inst = rm.open_resource(visaList[0])
        print(f"接続した機器: {inst}")
        result = inst.query("*IDN?")
        print(f"機器ID: {result}")
        inst.timeout = 10000  # ms

        print("信号発生器の周波数、出力減衰を変更して複数回測定します...")
        print("各測定の間で信号発生器の設定を変更してください")

        for measurement in range(3):
            print(f"\n--- 測定 {measurement + 1} ---")
            input(
                f"測定 {measurement + 1} の準備ができたらEnterキーを押してください..."
            )  # シングルショット測定に設定
            inst.write(":SINGle")
            time.sleep(0.1)  # 少し待機
            inst.query("*OPC?")  # 測定完了確認

            # ch1の波形を取得できるように設定
            inst.write(":WAVeform:SOURce CHANnel1")
            inst.write(":WAVeform:MODE NORMal")
            inst.write(":WAVeform:FORMat BYTE")

            # データ点数を取得
            acq_record = int(inst.query("WAVeform:POINts?"))

            # 軸のスケール情報を取得
            x_increment = float(inst.query(":WAVeform:XINCrement?"))
            x_origin = float(inst.query(":WAVeform:XORigin?"))
            x_reference = float(inst.query(":WAVeform:XREFerence?"))

            y_increment = float(inst.query(":WAVeform:YINCrement?"))
            y_origin = float(inst.query(":WAVeform:YORigin?"))
            y_reference = float(inst.query(":WAVeform:YREFerence?"))

            # 波形データを取得
            binwave1 = inst.query_binary_values(
                ":WAVeform:DATA?",
                datatype="B",
                container=list,
                chunk_size=acq_record * 1,
            )

            # 時間軸とデータをスケールに変換
            time_data = [
                (i - x_reference) * x_increment + x_origin for i in range(len(binwave1))
            ]
            voltage_data = [
                (data - y_reference) * y_increment + y_origin for data in binwave1
            ]

            # 波形の特徴量を計算
            max_voltage = max(voltage_data)
            min_voltage = min(voltage_data)
            amplitude = (max_voltage - min_voltage) / 2
            offset = (max_voltage + min_voltage) / 2

            # 周期の計算
            mean_voltage = np.mean(voltage_data)
            zero_crossings = []

            for i in range(len(voltage_data) - 1):
                if (voltage_data[i] - mean_voltage) * (
                    voltage_data[i + 1] - mean_voltage
                ) < 0:
                    t_cross = time_data[i] + (time_data[i + 1] - time_data[i]) * (
                        mean_voltage - voltage_data[i]
                    ) / (voltage_data[i + 1] - voltage_data[i])
                    zero_crossings.append(t_cross)

            # 周期計算
            positive_crossings = []
            for i in range(len(zero_crossings) - 1):
                idx = int(
                    (zero_crossings[i] - time_data[0]) / (time_data[1] - time_data[0])
                )
                if idx < len(voltage_data) - 1:
                    slope = voltage_data[idx + 1] - voltage_data[idx]
                    if slope > 0:
                        positive_crossings.append(zero_crossings[i])

            if len(positive_crossings) >= 2:
                periods = [
                    positive_crossings[i] - positive_crossings[i - 1]
                    for i in range(1, len(positive_crossings))
                ]
                average_period = np.mean(periods)
                frequency = 1 / average_period if average_period > 0 else 0
            else:
                average_period = 0
                frequency = 0

            print(f"測定結果 {measurement + 1}:")
            print(f"  振幅: {amplitude:.4f} V")
            print(f"  周波数: {frequency:.2f} Hz")
            print(
                f"  周期: {average_period * 1000:.4f} ms"
                if average_period > 0
                else "  周期: 計算不可"
            )
            print(f"  オフセット: {offset:.4f} V")
            print(f"  ピーク・ツー・ピーク: {max_voltage - min_voltage:.4f} V")

        # 自動測定に変更
        inst.write(":RUN")
        inst.close()

    else:
        print("接続可能な機器が見つかりません")

    rm.close()
