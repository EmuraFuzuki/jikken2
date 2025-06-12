import matplotlib.pyplot as plt
import numpy as np

# 課題9: アルキメデスの螺旋を5回転分表示
# 一回転するごとに半径が0.2増加

# パラメータt（0から10πまで：5回転分）
t = np.linspace(0, 10 * np.pi, 1000)

# アルキメデスの螺旋の座標
# r = a * θ の形で、ここではa = 0.2 / (2π) ≈ 0.0318
a = 0.2 / (2 * np.pi)
r = a * t

x = r * np.cos(t)
y = r * np.sin(t)

plt.plot(x, y, label="Archimedes' spiral (5 turns)", linewidth=2)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Archimedes' Spiral - 5 rotations, radius increases by 0.2 per turn")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()
