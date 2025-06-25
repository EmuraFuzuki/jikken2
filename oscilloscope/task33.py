# 課題33: オシロスコープで測定した波形データから振幅を求める
def main1():
    import pyvisa
    import numpy as np

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

        # シングルショット測定に設定
        inst.write(":SINGle")
        r = inst.query("*OPC?")
        print(f"測定完了確認: {r}")

        # ch1の波形を取得できるように設定
        inst.write(":WAVeform:SOURce CHANnel1")
        inst.write(":WAVeform:MODE NORMal")
        inst.write(":WAVeform:FORMat BYTE")

        # データ点数を取得
        acq_record = int(inst.query("WAVeform:POINts?"))
        # 軸のスケール情報を取得（Y軸のみ使用）
        # x_increment = float(inst.query(':WAVeform:XINCrement?'))
        # x_origin = float(inst.query(':WAVeform:XORigin?'))
        # x_reference = float(inst.query(':WAVeform:XREFerence?'))

        y_increment = float(inst.query(":WAVeform:YINCrement?"))
        y_origin = float(inst.query(":WAVeform:YORigin?"))
        y_reference = float(inst.query(":WAVeform:YREFerence?"))

        # 波形データを取得
        binwave1 = inst.query_binary_values(
            ":WAVeform:DATA?", datatype="B", container=list, chunk_size=acq_record * 1
        )

        # シングルショット測定にしていたのを自動測定に変更
        inst.write(":RUN")
        inst.close()  # データをスケールに変換（時間軸は今回使用しないため省略）
        # time_data = [(i - x_reference) * x_increment + x_origin for i in range(len(binwave1))]
        voltage_data = [
            (data - y_reference) * y_increment + y_origin for data in binwave1
        ]

        # 振幅を計算
        max_voltage = max(voltage_data)
        min_voltage = min(voltage_data)
        amplitude = (max_voltage - min_voltage) / 2
        offset = (max_voltage + min_voltage) / 2

        print("=== 波形解析結果 ===")
        print(f"最大電圧: {max_voltage:.4f} V")
        print(f"最小電圧: {min_voltage:.4f} V")
        print(f"振幅: {amplitude:.4f} V")
        print(f"オフセット: {offset:.4f} V")
        print(f"ピーク・ツー・ピーク: {max_voltage - min_voltage:.4f} V")

        # 統計情報も表示
        mean_voltage = np.mean(voltage_data)
        std_voltage = np.std(voltage_data)
        print(f"平均電圧: {mean_voltage:.4f} V")
        print(f"標準偏差: {std_voltage:.4f} V")

    else:
        print("接続可能な機器が見つかりません")

    rm.close()
