import matplotlib.pyplot as plt

x = [1, 4, 8]
y = [2, 11, 30]

plt.plot(x, y, label="my test")
plt.legend()
plt.xlabel("x-axis", fontsize=20)
plt.ylabel("y-axis", fontsize=30)

plt.show()
