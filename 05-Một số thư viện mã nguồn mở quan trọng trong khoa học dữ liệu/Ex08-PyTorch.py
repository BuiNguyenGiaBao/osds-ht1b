import torch
import torch.nn as nn
import torch.optim as optim

# Tạo dữ liệu mẫu
X = torch.tensor([[1.0], [2.0], [3.0], [4.0], [5.0]], dtype=torch.float32)
y = torch.tensor([[2.0], [4.1], [5.9], [7.2], [8.5]], dtype=torch.float32)

# Xây dựng mô hình
model = nn.Linear(1, 1)  # Một lớp linear với 1 input và 1 output

# Định nghĩa hàm loss và optimizer
criterion = nn.MSELoss()  # Mean Squared Error
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Huấn luyện mô hình
for epoch in range(1000):
    # Tính toán output
    outputs = model(X)
    
    # Tính toán loss
    loss = criterion(outputs, y)
    
    # Backpropagation và cập nhật trọng số
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{1000}], Loss: {loss.item():.4f}')

# Dự đoán
new_data = torch.tensor([[7.0]])
predicted = model(new_data)
print(predicted)