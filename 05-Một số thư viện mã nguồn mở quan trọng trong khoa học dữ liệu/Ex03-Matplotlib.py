import matplotlib.pyplot as plt
import numpy as np

# Tạo dữ liệu mẫu
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Tạo figure và các subplot
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

# Vẽ biểu đồ đường trên subplot đầu tiên
axes[0, 0].plot(x, y1)
axes[0, 0].set_title('Đồ thị sin')

# Vẽ biểu đồ phân tán trên subplot thứ hai
axes[0, 1].scatter(x, y2)
axes[0, 1].set_title('Đồ thị phân tán')

# Vẽ biểu đồ cột trên subplot thứ ba
axes[1, 0].bar(np.arange(5), np.random.rand(5))
axes[1, 0].set_title('Biểu đồ cột')

# Vẽ biểu đồ nhiệt độ trên subplot thứ tư
axes[1, 1].imshow(np.random.rand(10, 10), cmap='hot')
axes[1, 1].set_title('Biểu đồ nhiệt độ')

plt.tight_layout()
plt.show()