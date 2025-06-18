# 複数プロットの例
import matplotlib.pyplot as plt

# 一つ目のデータ
x1 = [1, 2, 3, 4]
y1 = [0.1, 2, 5, 11]

# 二つ目のデータ
x2 = [10, 20, 30, 40]
y2 = [-0.1, -2, -4, -1]

plt.plot(x1, y1, label="test 1", linestyle=":")
plt.legend()
# 折れ線グラフ1をプロット

plt.plot(x2, y2, label="test 2", marker=">")
plt.legend()
# 折れ線グラフ2をプロット

plt.show()
# グラフを表示
# 環境によってはグラフのウィンドウを閉じないと次の命令が実行されない

plt.savefig("1Dmulti.png")
# グラフをpng形式で保存
