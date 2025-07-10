import smbus
import time
import math


def main1():
    # MPU-6050 の I2C アドレス
    MPU_ADDR = 0x68

    # レジスタ定義
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B
    GYRO_XOUT_H = 0x43

    # I2C バス取得
    bus = smbus.SMBus(1)

    # MPU-6050 の起動
    bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0x00)
    time.sleep(0.1)

    def read_word(reg_h):
        high = bus.read_byte_data(MPU_ADDR, reg_h)
        low = bus.read_byte_data(MPU_ADDR, reg_h + 1)
        val = (high << 8) + low
        return val if val < 32768 else val - 65536

    def get_accel():
        ax = read_word(ACCEL_XOUT_H) / 16384.0
        ay = read_word(ACCEL_XOUT_H + 2) / 16384.0
        az = read_word(ACCEL_XOUT_H + 4) / 16384.0
        return ax, ay, az

    def get_gyro():
        gx = read_word(GYRO_XOUT_H) / 131.0
        gy = read_word(GYRO_XOUT_H + 2) / 131.0
        gz = read_word(GYRO_XOUT_H + 4) / 131.0
        return gx, gy, gz

    # 相補フィルタ係数
    alpha = 0.98

    # 初期角度：加速度センサだけで計算
    ax, ay, az = get_accel()
    roll = math.atan2(ay, az)
    pitch = math.atan2(-ax, math.sqrt(ay * ay + az * az))

    prev_time = time.time()

    while True:
        now = time.time()
        dt = now - prev_time
        prev_time = now

        ax, ay, az = get_accel()
        gx, gy, gz = get_gyro()

        # 加速度センサからの角度
        roll_acc = math.atan2(ay, az)
        pitch_acc = math.atan2(-ax, math.sqrt(ay * ay + az * az))

        # ジャイロからの角度増分
        roll += gx * dt * math.pi / 180.0
        pitch += gy * dt * math.pi / 180.0

        # 相補フィルタで融合
        roll = alpha * roll + (1 - alpha) * roll_acc
        pitch = alpha * pitch + (1 - alpha) * pitch_acc

        # 結果を度に変換
        print(f"Roll:  {math.degrees(roll): .2f}°, Pitch: {math.degrees(pitch): .2f}°")

        time.sleep(0.02)
