import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Tạo dữ liệu mẫu (bạn có thể thay thế bằng dữ liệu thực tế)
data = {'dientich': [100, 150, 200, 250, 300, 400, 500],
        'gia': [1000, 1500, 2000, 2500, 3000, 3250, 3300]}

# Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X = df[['dientich']]  # Tính năng (diện tích)
y = df['gia']  # Nhãn (giá)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tạo mô hình hồi quy tuyến tính
model = LinearRegression()

# Huấn luyện mô hình
model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá mô hình
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Vẽ đồ thị
plt.scatter(X_test, y_test, color='blue', label='Dữ liệu thực tế')
plt.plot(X_test, y_pred, color='red', label='Dự đoán')
plt.xlabel('Diện tích')
plt.ylabel('Giá')
plt.legend()
plt.show()