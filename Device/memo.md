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


(venvdir) guest1@raspberrypi:~/emura/jikken2 $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- ^C


uest1@raspberrypi:~/emura/jikken2 $ dmesg | grep -i i2c
[    0.902361] brcmstb-i2c 107d508200.i2c:  @97500hz registered in interrupt mode
[    0.908475] brcmstb-i2c 107d508280.i2c:  @97500hz registered in interrupt mode
[    2.450027] i2c_dev: i2c /dev entries driver
[  111.407719] i2c_designware 1f00074000.i2c: i2c_dw_handle_tx_abort: SDA stuck at low
[  112.419717] i2c_designware 1f00074000.i2c: controller timed out
[  113.443717] i2c_designware 1f00074000.i2c: controller timed out
[  114.467716] i2c_designware 1f00074000.i2c: controller timed out
[  115.491716] i2c_designware 1f00074000.i2c: controller timed out
[  116.515718] i2c_designware 1f00074000.i2c: controller timed out
[  117.539718] i2c_designware 1f00074000.i2c: controller timed out
[  118.563721] i2c_designware 1f00074000.i2c: controller timed out
[  119.587718] i2c_designware 1f00074000.i2c: controller timed out
[  120.611719] i2c_designware 1f00074000.i2c: controller timed out
[  298.755716] i2c_designware 1f00074000.i2c: controller timed out
[  306.947713] i2c_designware 1f00074000.i2c: controller timed out
[  418.627725] i2c_designware 1f00074000.i2c: controller timed out
[  419.651718] i2c_designware 1f00074000.i2c: controller timed out
[  420.675717] i2c_designware 1f00074000.i2c: controller timed out
[  421.699718] i2c_designware 1f00074000.i2c: controller timed out
[  422.723716] i2c_designware 1f00074000.i2c: controller timed out
[  423.747717] i2c_designware 1f00074000.i2c: controller timed out
[  424.771717] i2c_designware 1f00074000.i2c: controller timed out
[  425.795718] i2c_designware 1f00074000.i2c: controller timed out
[  426.819718] i2c_designware 1f00074000.i2c: controller timed out
[  427.843725] i2c_designware 1f00074000.i2c: controller timed out
[  428.867719] i2c_designware 1f00074000.i2c: controller timed out
[  429.891715] i2c_designware 1f00074000.i2c: controller timed out
[  430.915716] i2c_designware 1f00074000.i2c: controller timed out
[  687.651714] i2c_designware 1f00074000.i2c: controller timed out
[  688.675719] i2c_designware 1f00074000.i2c: controller timed out
[  689.699735] i2c_designware 1f00074000.i2c: controller timed out
[  690.723713] i2c_designware 1f00074000.i2c: controller timed out
[  691.747717] i2c_designware 1f00074000.i2c: controller timed out
[  692.771715] i2c_designware 1f00074000.i2c: controller timed out
[  693.795717] i2c_designware 1f00074000.i2c: controller timed out
[  694.819716] i2c_designware 1f00074000.i2c: controller timed out
[  695.843713] i2c_designware 1f00074000.i2c: controller timed out
[  696.867718] i2c_designware 1f00074000.i2c: controller timed out
[  697.891715] i2c_designware 1f00074000.i2c: controller timed out
[  698.915714] i2c_designware 1f00074000.i2c: controller timed out
[  699.939712] i2c_designware 1f00074000.i2c: controller timed out
[  700.963712] i2c_designware 1f00074000.i2c: controller timed out
[  701.987717] i2c_designware 1f00074000.i2c: controller timed out
[  703.011734] i2c_designware 1f00074000.i2c: controller timed out
[  704.035713] i2c_designware 1f00074000.i2c: controller timed out
[  705.059717] i2c_designware 1f00074000.i2c: controller timed out
[  706.083713] i2c_designware 1f00074000.i2c: controller timed out
[  707.107716] i2c_designware 1f00074000.i2c: controller timed out
[  708.131714] i2c_designware 1f00074000.i2c: controller timed out
[  709.155734] i2c_designware 1f00074000.i2c: controller timed out
[  710.179718] i2c_designware 1f00074000.i2c: controller timed out
[  711.203712] i2c_designware 1f00074000.i2c: controller timed out
[  712.227718] i2c_designware 1f00074000.i2c: controller timed out
[  713.251715] i2c_designware 1f00074000.i2c: controller timed out
[  714.275733] i2c_designware 1f00074000.i2c: controller timed out
[  715.299716] i2c_designware 1f00074000.i2c: controller timed out
[  716.323712] i2c_designware 1f00074000.i2c: controller timed out
[  717.347715] i2c_designware 1f00074000.i2c: controller timed out
[  718.371749] i2c_designware 1f00074000.i2c: controller timed out
[  719.395712] i2c_designware 1f00074000.i2c: controller timed out
[  720.419714] i2c_designware 1f00074000.i2c: controller timed out
[  721.443718] i2c_designware 1f00074000.i2c: controller timed out
[  722.467714] i2c_designware 1f00074000.i2c: controller timed out
[  723.491714] i2c_designware 1f00074000.i2c: controller timed out
[  724.515713] i2c_designware 1f00074000.i2c: controller timed out
[  725.539716] i2c_designware 1f00074000.i2c: controller timed out
[  726.563711] i2c_designware 1f00074000.i2c: controller timed out
[  727.587714] i2c_designware 1f00074000.i2c: controller timed out
[  728.611720] i2c_designware 1f00074000.i2c: controller timed out
[  729.635718] i2c_designware 1f00074000.i2c: controller timed out
[  730.659713] i2c_designware 1f00074000.i2c: controller timed out
[  731.683713] i2c_designware 1f00074000.i2c: controller timed out
[  732.707712] i2c_designware 1f00074000.i2c: controller timed out
[  733.731713] i2c_designware 1f00074000.i2c: controller timed out
[  734.755733] i2c_designware 1f00074000.i2c: controller timed out
[  735.779718] i2c_designware 1f00074000.i2c: controller timed out
[  736.803717] i2c_designware 1f00074000.i2c: controller timed out
[  737.827714] i2c_designware 1f00074000.i2c: controller timed out
[  738.851718] i2c_designware 1f00074000.i2c: controller timed out
[  739.875711] i2c_designware 1f00074000.i2c: controller timed out
[  740.899712] i2c_designware 1f00074000.i2c: controller timed out
[  741.923734] i2c_designware 1f00074000.i2c: controller timed out
[  742.947718] i2c_designware 1f00074000.i2c: controller timed out
[  743.971716] i2c_designware 1f00074000.i2c: controller timed out
[  744.995715] i2c_designware 1f00074000.i2c: controller timed out
[  746.019715] i2c_designware 1f00074000.i2c: controller timed out
[  747.043718] i2c_designware 1f00074000.i2c: controller timed out
[  748.067712] i2c_designware 1f00074000.i2c: controller timed out
[  749.091733] i2c_designware 1f00074000.i2c: controller timed out
[  750.115711] i2c_designware 1f00074000.i2c: controller timed out
[  751.139713] i2c_designware 1f00074000.i2c: controller timed out
[  752.163718] i2c_designware 1f00074000.i2c: controller timed out
[  753.187716] i2c_designware 1f00074000.i2c: controller timed out
[  754.211733] i2c_designware 1f00074000.i2c: controller timed out
[  755.235714] i2c_designware 1f00074000.i2c: controller timed out
[  756.259716] i2c_designware 1f00074000.i2c: controller timed out
[  757.283715] i2c_designware 1f00074000.i2c: controller timed out
[  758.307712] i2c_designware 1f00074000.i2c: controller timed out
[  759.331713] i2c_designware 1f00074000.i2c: controller timed out
[  760.355713] i2c_designware 1f00074000.i2c: controller timed out
[  761.379734] i2c_designware 1f00074000.i2c: controller timed out
[  762.403713] i2c_designware 1f00074000.i2c: controller timed out
[  763.427713] i2c_designware 1f00074000.i2c: controller timed out
[  764.451717] i2c_designware 1f00074000.i2c: controller timed out
[  765.475715] i2c_designware 1f00074000.i2c: controller timed out
[  766.499715] i2c_designware 1f00074000.i2c: controller timed out
[  767.523714] i2c_designware 1f00074000.i2c: controller timed out
[  768.547738] i2c_designware 1f00074000.i2c: controller timed out
[  769.571714] i2c_designware 1f00074000.i2c: controller timed out
[  770.595715] i2c_designware 1f00074000.i2c: controller timed out
[  771.619712] i2c_designware 1f00074000.i2c: controller timed out
[  772.643714] i2c_designware 1f00074000.i2c: controller timed out
[  773.667737] i2c_designware 1f00074000.i2c: controller timed out
[  774.691721] i2c_designware 1f00074000.i2c: controller timed out
[  775.715720] i2c_designware 1f00074000.i2c: controller timed out
[  776.739725] i2c_designware 1f00074000.i2c: controller timed out
[  777.763733] i2c_designware 1f00074000.i2c: controller timed out
[  778.787723] i2c_designware 1f00074000.i2c: controller timed out
[  779.811723] i2c_designware 1f00074000.i2c: controller timed out
[  780.835721] i2c_designware 1f00074000.i2c: controller timed out
[  781.859718] i2c_designware 1f00074000.i2c: controller timed out
[  782.883719] i2c_designware 1f00074000.i2c: controller timed out
[  783.907726] i2c_designware 1f00074000.i2c: controller timed out
[  784.931722] i2c_designware 1f00074000.i2c: controller timed out
[  785.955721] i2c_designware 1f00074000.i2c: controller timed out
[  786.979727] i2c_designware 1f00074000.i2c: controller timed out
[  788.003723] i2c_designware 1f00074000.i2c: controller timed out
[  789.027721] i2c_designware 1f00074000.i2c: controller timed out
[  790.051717] i2c_designware 1f00074000.i2c: controller timed out
[  791.075712] i2c_designware 1f00074000.i2c: controller timed out
[  792.099712] i2c_designware 1f00074000.i2c: controller timed out
[  793.123714] i2c_designware 1f00074000.i2c: controller timed out
[  794.147712] i2c_designware 1f00074000.i2c: controller timed out
[  795.171712] i2c_designware 1f00074000.i2c: controller timed out
[  796.195712] i2c_designware 1f00074000.i2c: controller timed out
[  797.219716] i2c_designware 1f00074000.i2c: controller timed out
[  798.243711] i2c_designware 1f00074000.i2c: controller timed out
[  799.267714] i2c_designware 1f00074000.i2c: controller timed out
[  800.291710] i2c_designware 1f00074000.i2c: controller timed out
[  801.315711] i2c_designware 1f00074000.i2c: controller timed out
[  961.155714] i2c_designware 1f00074000.i2c: controller timed out
guest1@raspberrypi:~/emura/jikken2 $ 

