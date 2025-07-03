def main1():
    #!/usr/bin/env python3
    import smbus
    import time

    # MPU6050 レジスタ定義
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B
    GYRO_XOUT_H = 0x43

    def read_raw_data(addr):
        high = bus.read_byte_data(DEVICE_ADDRESS, addr)
        low = bus.read_byte_data(DEVICE_ADDRESS, addr + 1)
        value = (high << 8) | low
        if value > 32767:
            value -= 65536
        return value

    # I2C バス、デバイスアドレスの設定
    bus = smbus.SMBus(1)  # Raspberry Pi の I2C バス番号
    DEVICE_ADDRESS = 0x68  # MPU6050 のデフォルトアドレス

    # センサーをウェイクアップ
    bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 0)

    time.sleep(1)
    print("MPU6050 初期化完了。データを取得中…\n")

    try:
        while True:
            # 生データ取得
            acc_x = read_raw_data(ACCEL_XOUT_H)
            acc_y = read_raw_data(ACCEL_XOUT_H + 2)
            acc_z = read_raw_data(ACCEL_XOUT_H + 4)

            gyro_x = read_raw_data(GYRO_XOUT_H)
            gyro_y = read_raw_data(GYRO_XOUT_H + 2)
            gyro_z = read_raw_data(GYRO_XOUT_H + 4)

            # 感度スケール変換
            Ax = acc_x / 16384.0  # ±2g モード → 1g = 16384 LSB
            Ay = acc_y / 16384.0
            Az = acc_z / 16384.0

            Gx = gyro_x / 131.0  # ±250°/s モード → 1°/s = 131 LSB
            Gy = gyro_y / 131.0
            Gz = gyro_z / 131.0

            # 結果表示
            print(f"加速度 [g]   : X = {Ax:.2f}, Y = {Ay:.2f}, Z = {Az:.2f}")
            print(f"ジャイロ [°/s]: X = {Gx:.2f}, Y = {Gy:.2f}, Z = {Gz:.2f}")
            print("-------------------------------")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n終了します。")
