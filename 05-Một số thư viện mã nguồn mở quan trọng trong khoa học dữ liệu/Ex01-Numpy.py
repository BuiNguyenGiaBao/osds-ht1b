import numpy as np

# Tạo các mảng
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# Các phép toán
result1 = arr1 + arr2  # Sẽ báo lỗi vì kích thước không tương thích
result2 = arr1 * 2
result3 = np.mean(arr2, axis=1)  # Trung bình theo hàng

# Indexing và slicing
element = arr1[2]
subarray = arr2[:, 1]

# Thao tác với mảng
arr3 = arr1.reshape(5, 1)
sorted_arr = np.sort(arr2, axis=0)

# Hàm toán học
sin_values = np.sin(arr1)
dot_product = np.dot(arr1, arr1)

# In kết quả
print("arr1:", arr1)
print("result2:", result2)
print("result3:", result3)
print("element:", element)
print("subarray:", subarray)
print("arr3:", arr3)
print("sorted_arr:", sorted_arr)
print("sin_values:", sin_values)
print("dot_product:", dot_product)