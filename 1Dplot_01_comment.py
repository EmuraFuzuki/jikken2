import matplotlib.pyplot as plt
# matplotlib内のプロット機能pypplotを呼び出す
# 以下で使うときはpltとして呼び出す

x = [1, 4, 8]
y = [2, 11, 30]
# x, yのデータ点をそれぞれ1次元配列で表す。

plt.plot(x, y, label="my test")
# plot()はpyplotが持つメソッド(関数)
# 第1引数: 横軸のデータ点を表す配列, 第2引数: 縦軸のデータ点を表す配列、
# 第3以降の引数: 各種プロパティの設定

plt.legend()
# グラフ上に凡例を表示するように設定

plt.xlabel("x-axis", fontsize=20)
plt.ylabel("y-axis", fontsize=30)
# 縦軸、横軸にラベルを挿入する
# 文字の大きさはfontsizeで設定可能

plt.show()
# 上で設定したグラフを表示させる
