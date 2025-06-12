# 計測器
## モーションセンサ
手をかざすと反応する
## 温度センサ
気温が高いときに動作する
## 照度センサ
光の強さを測定する
## 距離センサ
画面に近いと反応する

# 出力デバイス
## 4連セグメントディスプレイ
時間を表示する
## LED
警告などを表示する
## ブザー
音を鳴らす
## モータ
送風する
## バーグラフ
気温を段階的に表示する



Traceback (most recent call last):
  File "/home/guest1/emura/jikken2/main.py", line 6, in <module>
    main1()
  File "/home/guest1/emura/jikken2/Device/motion_sensor_test.py", line 11, in main1
    GPIO.setup(SENSOR_PIN, GPIO.IN)  # SENSOR_PINを入力モードに設定
RuntimeError: Cannot determine SOC peripheral base address
