# 課題28: 測定したデータをグラフに表示
def main1():
    import pyvisa
    import matplotlib.pyplot as plt

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
        print(f"データ点数: {acq_record}")

        # 軸のスケール情報を取得
        x_increment = float(inst.query(":WAVeform:XINCrement?"))
        x_origin = float(inst.query(":WAVeform:XORigin?"))
        x_reference = float(inst.query(":WAVeform:XREFerence?"))

        y_increment = float(inst.query(":WAVeform:YINCrement?"))
        y_origin = float(inst.query(":WAVeform:YORigin?"))
        y_reference = float(inst.query(":WAVeform:YREFerence?"))

        print(
            f"X increment: {x_increment}, X origin: {x_origin}, X reference: {x_reference}"
        )
        print(
            f"Y increment: {y_increment}, Y origin: {y_origin}, Y reference: {y_reference}"
        )

        # 波形データを取得
        binwave1 = inst.query_binary_values(
            ":WAVeform:DATA?", datatype="B", container=list, chunk_size=acq_record * 1
        )

        # シングルショット測定にしていたのを自動測定に変更
        inst.write(":RUN")
        inst.close()

        # 時間軸とデータをスケールに変換
        time_data = [
            (i - x_reference) * x_increment + x_origin for i in range(len(binwave1))
        ]
        voltage_data = [
            (data - y_reference) * y_increment + y_origin for data in binwave1
        ]

        # グラフを表示
        plt.figure(figsize=(10, 6))
        plt.plot(time_data, voltage_data)
        plt.xlabel("Time [s]")
        plt.ylabel("Voltage [V]")
        plt.title("Oscilloscope Waveform")
        plt.grid(True)
        plt.show()

    else:
        print("接続可能な機器が見つかりません")

    rm.close()
