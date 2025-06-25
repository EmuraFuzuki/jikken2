# 課題36: ノイズの影響を受けにくい特徴量抽出の工夫
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
        inst.query("*OPC?")

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

        # 自動測定に変更
        inst.write(":RUN")
        inst.close()  # データをスケールに変換（時間軸は今回使用しないため省略）
        # time_data = [(i - x_reference) * x_increment + x_origin for i in range(len(binwave1))]
        voltage_data = [
            (data - y_reference) * y_increment + y_origin for data in binwave1
        ]

        print("=== ノイズ対策を含む波形解析 ===")

        # 1. 移動平均フィルタによるノイズ除去
        def moving_average(data, window_size):
            """移動平均フィルタ"""
            if window_size >= len(data):
                return data
            filtered_data = []
            for i in range(len(data)):
                start = max(0, i - window_size // 2)
                end = min(len(data), i + window_size // 2 + 1)
                filtered_data.append(np.mean(data[start:end]))
            return filtered_data

        # 2. 振幅の計算（複数の手法）
        # 生データから計算
        raw_amplitude = (max(voltage_data) - min(voltage_data)) / 2

        # 移動平均フィルタ適用後
        filtered_data = moving_average(voltage_data, 5)
        filtered_amplitude = (max(filtered_data) - min(filtered_data)) / 2

        # パーセンタイル法（外れ値に強い）
        percentile_95 = np.percentile(voltage_data, 95)
        percentile_5 = np.percentile(voltage_data, 5)
        percentile_amplitude = (percentile_95 - percentile_5) / 2

        # 3. オフセットの計算（複数の手法）
        mean_offset = np.mean(voltage_data)
        median_offset = np.median(voltage_data)  # 外れ値に強い
        filtered_offset = np.mean(filtered_data)

        # 4. 実効値計算（ノイズを含む真の実効値）
        rms_raw = np.sqrt(np.mean([v**2 for v in voltage_data]))
        rms_filtered = np.sqrt(np.mean([v**2 for v in filtered_data]))

        print("振幅の計算結果:")
        print(f"  生データ: {raw_amplitude:.4f} V")
        print(f"  フィルタ後: {filtered_amplitude:.4f} V")
        print(f"  パーセンタイル法: {percentile_amplitude:.4f} V")

        print("\nオフセットの計算結果:")
        print(f"  平均値: {mean_offset:.4f} V")
        print(f"  中央値: {median_offset:.4f} V")
        print(f"  フィルタ後平均: {filtered_offset:.4f} V")

        print("\n実効値の計算結果:")
        print(f"  生データ: {rms_raw:.4f} V")
        print(f"  フィルタ後: {rms_filtered:.4f} V")

        # 5. ノイズレベルの推定
        noise_std = np.std(np.diff(voltage_data))  # 隣接点の差分の標準偏差
        snr_estimate = filtered_amplitude / noise_std if noise_std > 0 else float("inf")

        print("\nノイズ解析:")
        print(f"  推定ノイズレベル: {noise_std:.6f} V")
        print(f"  推定S/N比: {snr_estimate:.1f}")

        print("\n=== ノイズ対策の推奨事項 ===")
        print("1. 移動平均フィルタ: 高周波ノイズの除去")
        print("2. パーセンタイル法: 突発的なノイズに強い")
        print("3. 中央値使用: 外れ値の影響を軽減")
        print("4. 複数回測定の平均: ランダムノイズの低減")
        print("5. 適切なサンプリング設定: オーバーサンプリング")

    else:
        print("接続可能な機器が見つかりません")

    rm.close()
