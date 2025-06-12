import matplotlib.pyplot as plt
import numpy as np

# 課題11: 円と螺旋と花びらを同時に表示して"ハナマル"を作成

# パラメータt
t = np.linspace(0, 10 * np.pi, 1000)

# 円の座標（半径1）
t_circle = np.linspace(0, 2 * np.pi, 1000)
x_circle = np.cos(t_circle)
y_circle = np.sin(t_circle)

# アルキメデスの螺旋の座標
a = 0.2 / (2 * np.pi)
r_spiral = a * t
x_spiral = r_spiral * np.cos(t)
y_spiral = r_spiral * np.sin(t)

# 花びらの座標（バラ曲線：r = cos(nθ)）
# 花びらを8枚にする
n = 4  # cos(4θ)で8枚の花びら
t_flower = np.linspace(0, 2 * np.pi, 1000)
r_flower = 0.8 * np.abs(np.cos(n * t_flower))  # 半径を少し小さくして調整
x_flower = r_flower * np.cos(t_flower)
y_flower = r_flower * np.sin(t_flower)

# グラフに表示
plt.figure(figsize=(10, 10))
plt.plot(x_circle, y_circle, label="Circle", linewidth=2, color='blue')
plt.plot(x_spiral, y_spiral, label="Archimedes' spiral", linewidth=1.5, color='green')
plt.plot(x_flower, y_flower, label="Flower petals", linewidth=2, color='red')

plt.xlabel("x")
plt.ylabel("y")
plt.title("ハナマル (Flower Circle): Circle + Spiral + Petals")
plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
