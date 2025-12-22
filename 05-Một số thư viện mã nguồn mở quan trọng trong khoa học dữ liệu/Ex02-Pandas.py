import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv("diem_hoc_sinh.csv")

# Hiển thị 5 dòng đầu tiên
print(df.head())

# Thông tin về DataFrame
print(df.info())

# Tính điểm trung bình các môn
df['Điểm trung bình'] = df[['Toán', 'Lý', 'Hóa']].mean(axis=1)

# Lọc học sinh có điểm Toán trên 8
hoc_sinh_gioi_toan = df[df['Toán'] > 8]

# Nhóm học sinh theo giới tính (giả sử có cột "Giới tính") và tính điểm trung bình mỗi nhóm
df.groupby('Giới tính')['Điểm trung bình'].mean()

# Lưu kết quả vào file Excel
df.to_excel("ket_qua.xlsx", index=False)



