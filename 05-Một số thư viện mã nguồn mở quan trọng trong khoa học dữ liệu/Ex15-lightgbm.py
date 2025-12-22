#!pip install  dask-expr 
import lightgbm as lgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# Load dữ liệu
data = load_breast_cancer()
X, y = data.data, data.target

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tạo dataset cho LightGBM
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test)

# Thiết lập các tham số
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9
}

# Huấn luyện mô hình
gbm = lgb.train(params,
                train_data,
                num_boost_round=100,
                valid_sets=test_data,
                early_stopping_rounds=10)

# Dự đoán trên tập kiểm tra
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)