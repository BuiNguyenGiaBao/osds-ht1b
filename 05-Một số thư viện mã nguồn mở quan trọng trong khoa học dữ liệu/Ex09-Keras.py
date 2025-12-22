import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Tạo dữ liệu mẫu
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 6])

# Xây dựng mô hình
model = Sequential([
    Dense(units=1, input_shape=[1])
])

# Biên dịch mô hình
model.compile(optimizer='sgd', loss='mean_squared_error')

# Huấn luyện mô hình
model.fit(X, y, epochs=500)

# Dự đoán
print(model.predict([10.0]))