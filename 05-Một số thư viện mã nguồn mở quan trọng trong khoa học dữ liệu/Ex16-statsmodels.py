import statsmodels.api as sm
import pandas as pd
import numpy as np

# Tạo dữ liệu mẫu
np.random.seed(0)
x = np.random.rand(100)
y = 2 * x + 1 + np.random.randn(100)

# Tạo DataFrame
df = pd.DataFrame({'x': x, 'y': y})

# Thêm hằng số vào biến độc lập
X = sm.add_constant(df['x'])

# Xây dựng mô hình hồi quy tuyến tính
model = sm.OLS(df['y'], X)
results = model.fit()

# In kết quả
print(results.summary())