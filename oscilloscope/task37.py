# 課題37: フーリエ変換を用いた波形データの特徴量抽出
def main1():
    import pyvisa
    import numpy as np
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
        inst.query("*OPC?")

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
            ":WAVeform:DATA?", datatype="B", container=list, chunk_size=acq_record * 1
        )

        # 自動測定に変更
        inst.write(":RUN")
        inst.close()

        # 時間軸とデータをスケールに変換
        time_data = [
            (i - x_reference) * x_increment + x_origin for i in range(len(binwave1))
        ]
        voltage_data = [
            (data - y_reference) * y_increment + y_origin for data in binwave1
        ]

        print("=== フーリエ変換による波形解析 ===")

        # フーリエ変換の実行
        # DCオフセットを除去
        voltage_data_centered = voltage_data - np.mean(voltage_data)

        # FFTを実行
        fft_result = np.fft.fft(voltage_data_centered)
        fft_freq = np.fft.fftfreq(len(voltage_data_centered), x_increment)

        # 振幅スペクトラムを計算
        amplitude_spectrum = np.abs(fft_result)

        # 正の周波数のみを取得
        positive_freq_mask = fft_freq > 0
        positive_frequencies = fft_freq[positive_freq_mask]
        positive_amplitudes = amplitude_spectrum[positive_freq_mask]

        # 基本周波数（最大ピーク）を見つける
        max_peak_index = np.argmax(positive_amplitudes)
        fundamental_frequency = positive_frequencies[max_peak_index]
        fundamental_amplitude = positive_amplitudes[max_peak_index]

        # 振幅をピーク値に変換（FFTの結果をデータ長で正規化）
        peak_amplitude = fundamental_amplitude * 2 / len(voltage_data)

        # 位相を計算
        fundamental_phase = np.angle(fft_result[max_peak_index + 1])  # +1は正の周波数側

        # 高調波を検出
        harmonics = []
        for n in range(2, 6):  # 2次から5次高調波まで
            harmonic_freq = fundamental_frequency * n
            # 最も近い周波数を見つける
            freq_diff = np.abs(positive_frequencies - harmonic_freq)
            if np.min(freq_diff) < fundamental_frequency * 0.1:  # 10%の誤差範囲内
                harmonic_index = np.argmin(freq_diff)
                harmonic_amplitude = (
                    positive_amplitudes[harmonic_index] * 2 / len(voltage_data)
                )
                harmonics.append((n, harmonic_freq, harmonic_amplitude))

        # 時間領域での解析結果
        max_voltage = max(voltage_data)
        min_voltage = min(voltage_data)
        time_domain_amplitude = (max_voltage - min_voltage) / 2
        dc_offset = np.mean(voltage_data)

        print("周波数領域解析結果:")
        print(f"  基本周波数: {fundamental_frequency:.2f} Hz")
        print(f"  基本波振幅: {peak_amplitude:.4f} V")
        print(
            f"  位相: {fundamental_phase:.2f} rad ({fundamental_phase * 180 / np.pi:.1f} deg)"
        )
        print(f"  DCオフセット: {dc_offset:.4f} V")

        if harmonics:
            print("\n検出された高調波:")
            for order, freq, amp in harmonics:
                thd_percent = (amp / peak_amplitude) * 100 if peak_amplitude > 0 else 0
                print(
                    f"  {order}次高調波: {freq:.2f} Hz, 振幅: {amp:.4f} V ({thd_percent:.1f}%)"
                )

        print("\n時間領域解析結果（比較用）:")
        print(f"  振幅: {time_domain_amplitude:.4f} V")
        print("  推定周波数: データ不足のため計算困難")

        # FFTの結果をプロット
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 1, 1)
        plt.plot([t * 1000 for t in time_data], voltage_data)
        plt.xlabel("Time [ms]")
        plt.ylabel("Voltage [V]")
        plt.title("Time Domain Signal")
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.plot(positive_frequencies, positive_amplitudes * 2 / len(voltage_data))
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Amplitude [V]")
        plt.title("Frequency Domain (FFT)")
        plt.grid(True)
        plt.xlim(
            0, min(1000, max(positive_frequencies))
        )  # 1kHzまでまたはデータの最大周波数

        plt.tight_layout()
        plt.show()

        print("\n=== フーリエ変換の利点 ===")
        print("1. 正確な周波数測定")
        print("2. 高調波歪みの検出")
        print("3. ノイズの周波数成分分析")
        print("4. 複数の信号成分の分離")

    else:
        print("接続可能な機器が見つかりません")

    rm.close()
