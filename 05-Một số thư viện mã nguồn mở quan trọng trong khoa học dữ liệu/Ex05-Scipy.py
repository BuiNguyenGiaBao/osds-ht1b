import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

# Ma trận hệ số
A = np.array([[2, 3],
              [1, -1]])

# Ma trận cột các số hạng tự do
b = np.array([7, 1])

# Giải hệ phương trình
x = solve(A, b)
print("Nghiệm của hệ phương trình là:", x)

# Vẽ đồ thị
x_values = np.linspace(-5, 5, 100)
y1 = (7 - 2 * x_values) / 3
y2 = x_values - 1

plt.plot(x_values, y1, label='2x + 3y = 7')
plt.plot(x_values, y2, label='x - y = 1')
plt.scatter(x[0], x[1], color='red', label='Nghiệm')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Giải hệ phương trình bậc nhất hai ẩn')
plt.legend()
plt.grid(True)
plt.show()