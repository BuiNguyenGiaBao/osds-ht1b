import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib

# Tải hình ảnh từ internet
url = 'https://upload.wikimedia.org/wikipedia/ru/2/24/Lenna.png'
img_resp = urllib.request.urlopen(url)
img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

# Chuyển ảnh thành ảnh xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Hiển thị ảnh gốc và ảnh xám
plt.figure(figsize=(10,5))
plt.subplot(1,2,1),plt.imshow(img[:,:,::-1]),plt.title('Original Image')
plt.subplot(1,2,2),plt.imshow(gray, cmap='gray'),plt.title('Gray Image')
plt.show()