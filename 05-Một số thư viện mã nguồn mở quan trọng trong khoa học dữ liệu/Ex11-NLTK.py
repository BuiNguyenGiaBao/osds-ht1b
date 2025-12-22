import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Tải dữ liệu
nltk.download('punkt')

# Đoạn văn bản mẫu
text = "Đây là một ví dụ về cách sử dụng NLTK để token hóa văn bản. Chúng ta sẽ tách câu và tách từ."

# Tách câu
sentences = sent_tokenize(text)
print(sentences)

# Tách từ trong câu đầu tiên
words = word_tokenize(sentences[0])
print(words)