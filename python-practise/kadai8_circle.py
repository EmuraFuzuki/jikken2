import matplotlib.pyplot as plt
import numpy as np

# 課題8: 原点(0,0)に中心をもつ半径1をもつ円を表示

# パラメータt（0から2πまで）
t = np.linspace(0, 2 * np.pi, 1000)

# 円の座標
x = np.cos(t)
y = np.sin(t)

plt.plot(x, y, label="Circle (radius=1)", linewidth=2)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Circle centered at origin with radius 1")
plt.axis("equal")  # 縦横の比率を等しくする
plt.grid(True)
plt.legend()
plt.show()
