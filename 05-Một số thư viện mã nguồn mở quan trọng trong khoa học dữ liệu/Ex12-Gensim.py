import gensim
from gensim.models import Word2Vec

# Tạo một danh sách các câu
sentences = [
    ['cat', 'sat', 'on', 'the', 'mat'],
    ['the', 'dog', 'barked', 'at', 'the', 'cat'],
]

# Tạo mô hình Word2Vec
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# Lưu mô hình
model.save("word2vec.model")

# Tải mô hình đã lưu
model = Word2Vec.load("word2vec.model")

# Xem vector của từ "cat"
print(model.wv['cat'])

# Tìm các từ tương tự với từ "cat"
print(model.wv.most_similar('cat'))