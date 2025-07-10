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


# For more options and information see
# http://rptl.io/configtxt
# Some settings may impact device functionality. See link above for details

# Uncomment some or all of these to enable the optional hardware interfaces
dtparam=i2c_arm=on
#dtparam=i2s=on
#dtparam=spi=on

# Enable audio (loads snd_bcm2835)
dtparam=audio=on

# Additional overlays and parameters are documented
# /boot/firmware/overlays/README

# Automatically load overlays for detected cameras
camera_auto_detect=1

# Automatically load overlays for detected DSI displays
display_auto_detect=1

# Automatically load initramfs files, if found
auto_initramfs=1

# Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d
max_framebuffers=2

# Don't have the firmware create an initial video= setting in cmdline.txt.
# Use the kernel's default instead.
disable_fw_kms_setup=1

# Run in 64-bit mode
arm_64bit=1

# Disable compensation for displays with overscan
disable_overscan=1

# Run as fast as firmware / board allows
arm_boost=1

[cm4]
# Enable host mode on the 2711 built-in XHCI USB controller.
# This line should be removed if the legacy DWC2 controller is required
# (e.g. for USB device mode) or if USB support is not required.
otg_mode=1

[cm5]
dtoverlay=dwc2,dr_mode=host

[all]


>>> %Run main.py
Traceback (most recent call last):
  File "/home/guest1/emura/jikken2/main.py", line 6, in <module>
    main1()
  File "/home/guest1/emura/jikken2/Device/MPU6050test.py", line 24, in main1
    bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 0)
TimeoutError: [Errno 110] Connection timed out



Roll:  -61.20°, Pitch: -81.20°
Roll:  -61.83°, Pitch: -83.49°
Roll:  -62.28°, Pitch: -84.87°
Roll:  -62.85°, Pitch: -86.55°
Roll:  -63.89°, Pitch: -87.04°
Roll:  -65.53°, Pitch: -87.35°
Roll:  -66.70°, Pitch: -88.34°
Roll:  -67.83°, Pitch: -89.11°
Roll:  -69.47°, Pitch: -89.28°
Roll:  -70.25°, Pitch: -90.07°
Roll:  -71.50°, Pitch: -89.53°
Roll:  -72.98°, Pitch: -87.62°
Roll:  -72.98°, Pitch: -87.34°
Roll:  -73.62°, Pitch: -86.52°



# 7/10

手ぶくろ入力装置を初期化しています...
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 393, in _gpio_list
    return tuple(_to_gpio(int(channel)) for channel in chanlist)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'int' object is not iterable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/guest1/emura/jikken2/Device/main.py", line 86, in <module>
    main()
  File "/home/guest1/emura/jikken2/Device/main.py", line 81, in main
    device = GloveInputDevice()
             ^^^^^^^^^^^^^^^^^^
  File "/home/guest1/emura/jikken2/Device/main.py", line 23, in __init__
    self.hcsr04 = HCSR04()
                  ^^^^^^^^
  File "/home/guest1/emura/jikken2/Device/utils/sensors.py", line 65, in __init__
    GPIO.setup(TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 680, in setup
    for gpio in _gpio_list(chanlist):
                ^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 396, in _gpio_list
    return (_to_gpio(int(chanlist)),)
            ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 356, in _to_gpio
    raise RuntimeError(
RuntimeError: Please set pin numbering mode using GPIO.setmode(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)


