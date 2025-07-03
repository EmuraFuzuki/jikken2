import smbus
import time
import sys

# レジスタ定義
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43


def read_raw_data(bus, addr, reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)
    value = (high << 8) | low
    return value - 65536 if value > 32767 else value


def detect_device_address(bus):
    for tentative in (0x68, 0x69):
        try:
            bus.write_byte_data(tentative, PWR_MGMT_1, 0)
            return tentative
        except OSError:
            continue
    return None


def main1():
    bus = smbus.SMBus(1)
    addr = detect_device_address(bus)
    if addr is None:
        print(
            "MPU6050 が 0x68/0x69 で検出できません。配線・I2C設定・AD0ピンを確認してください。"
        )
        sys.exit(1)

    print(f"MPU6050 アドレス: 0x{addr:02X}")
    # ウェイクアップ
    bus.write_byte_data(addr, PWR_MGMT_1, 0)
    time.sleep(1)
    print("初期化完了。データ取得を開始します。\n")

    try:
        while True:
            # 加速度取得
            ax = read_raw_data(bus, addr, ACCEL_XOUT_H) / 16384.0
            ay = read_raw_data(bus, addr, ACCEL_XOUT_H + 2) / 16384.0
            az = read_raw_data(bus, addr, ACCEL_XOUT_H + 4) / 16384.0
            # ジャイロ取得
            gx = read_raw_data(bus, addr, GYRO_XOUT_H) / 131.0
            gy = read_raw_data(bus, addr, GYRO_XOUT_H + 2) / 131.0
            gz = read_raw_data(bus, addr, GYRO_XOUT_H + 4) / 131.0

            print(f"加速度 [g]   : X={ax:.2f}, Y={ay:.2f}, Z={az:.2f}")
            print(f"ジャイロ [°/s]: X={gx:.2f}, Y={gy:.2f}, Z={gz:.2f}")
            print("-------------------------------")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n終了します。")
