import matplotlib.pyplot as plt
import numpy as np

# 課題7: なめらかなsin関数を書く
# 横軸の範囲0から2πに波が5回振動している

# x軸のデータ点を生成（0から2πまで）
x = np.linspace(0, 2 * np.pi, 1000)
# 5回振動させるため、xに5を掛ける
y = np.sin(5 * x)

plt.plot(x, y, label="sin(5x)", linewidth=2)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Sin function with 5 oscillations")
plt.grid(True)
plt.legend()
plt.show()
