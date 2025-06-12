import matplotlib.pyplot as plt
import numpy as np

# 課題10: sin関数とcos関数を同時に表示（同じ振動数）

# x軸のデータ点を生成（0から2πまで）
x = np.linspace(0, 2 * np.pi, 1000)
# 5回振動させる
y_sin = np.sin(5 * x)
y_cos = np.cos(5 * x)

plt.plot(x, y_sin, label="sin(5x)", linewidth=2, linestyle='-')
plt.plot(x, y_cos, label="cos(5x)", linewidth=2, linestyle='--')
plt.xlabel("x")
plt.ylabel("y")
plt.title("Sin and Cos functions with same frequency")
plt.grid(True)
plt.legend()
plt.show()
