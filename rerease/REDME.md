# ラズパイを用いた入力装置

## 機能
手の動きによる入力を取得する

### 詳細
#### 角速度入力
手袋に装着したジャイロセンサのx, y, z軸の角速度が一定以上になったときにそれぞれの入力信号を出力する。出力先はそれぞれ、黃、青、緑のLEDに接続する。
#### 距離入力
超音波センサを使用して入力を行う。センサとの距離が0~5cm, 5~10cm, 10~15cmの位置で1.0sec以上の間検出されたときにそれぞれ1個、2個、3個の赤色LEDを点灯させる。また、エアタップの動きを検出したときに、赤色LEDを点滅させる。

## ファイル構成
- `main.py` - メイン実行ファイル
- `config.py` - 設定ファイル（GPIO ピン番号、定数）
- `sensors.py` - センサー関連のクラス（MPU6050, HC-SR04, エアタップ検出）
- `gpio_controller.py` - GPIO制御クラス
- `test_main.py` - テスト用スクリプト
- `docx/demo.py` - 元のデモファイル（参考用）

## 実行方法
```bash
# メインプログラムを実行
python main.py

# テストスクリプトを実行（Raspberry Pi以外でも動作確認可能）
python test_main.py
```

## pythonモジュール
- smbus
- time
- RPi.GPIO

## センサ
- MPU6050
- Ultrasonic Ranging Module (HC-SR04)