# 課題27: オシロスコープから波形データを取得
def main1():
    import pyvisa

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
        # 測定が終了していると1が表示される
        r = inst.query("*OPC?")
        print(f"測定完了確認: {r}")

        # ch1の波形を取得できるように設定
        inst.write(":WAVeform:SOURce CHANnel1")
        inst.write(":WAVeform:MODE NORMal")
        # バイナリデータで送信
        inst.write(":WAVeform:FORMat BYTE")
        # データ点数を取得
        acq_record = int(inst.query("WAVeform:POINts?"))
        print(f"データ点数: {acq_record}")

        # 波形データを取得
        binwave1 = inst.query_binary_values(
            ":WAVeform:DATA?", datatype="B", container=list, chunk_size=acq_record * 1
        )

        # シングルショット測定にしていたのを自動測定に変更
        inst.write(":RUN")
        # instのインスタンスを閉じる
        inst.close()

        # データを確認
        print(f"取得したデータ長: {len(binwave1)}")
        print(f"最初の10個のデータ: {binwave1[:10]}")

    else:
        print("接続可能な機器が見つかりません")

    # rmのインスタンスを閉じる
    rm.close()
