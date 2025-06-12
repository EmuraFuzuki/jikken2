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


