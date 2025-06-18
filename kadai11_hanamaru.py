import matplotlib.pyplot as plt
import numpy as np

# 円の半径
R = 1.0


# θ を 0→2π
theta = np.linspace(0, 2 * np.pi, 1000)

# 円
x_circle = R * np.cos(theta)
y_circle = R * np.sin(theta)

# アルキメデスの螺旋の座標
# パラメータt
t = np.linspace(0, 10 * np.pi, 1000)
a = 0.2 / (2 * np.pi)
r_spiral = a * t
x_spiral = r_spiral * np.cos(t)
y_spiral = r_spiral * np.sin(t)


# 花びらの張り出し量
a = 0.2

# 花びら枚数：cos(4θ) で 8 枚
n = 4

# 花びら（絶対値を取って円の内側を消す）
r_petal = R + a * np.abs(np.cos(n * theta))
x_petal = r_petal * np.cos(theta)
y_petal = r_petal * np.sin(theta)

plt.figure(figsize=(6, 6))
plt.plot(x_circle, y_circle, linewidth=2, color="red", label="Circle")
plt.plot(x_spiral, y_spiral, linewidth=2, color="red", label="Spiral")
plt.plot(x_petal, y_petal, linewidth=2, color="red", label="Petals")

plt.axis("equal")
plt.grid(alpha=0.3)
plt.legend()
plt.show()
