import re
from collections import Counter

def count_different_words(file1, file2, time):
    def remove_punctuation_and_lowercase(text):
    # Loại bỏ dấu câu và chuyển thành chữ thường
      text_without_punctuation = re.sub(r'[^\w\s]', '', text)
    # Xóa các dấu cách thừa
      cleaned_text = re.sub(r'\s+', ' ', text_without_punctuation).strip()
      return cleaned_text.lower()
    def words(text):
      return re.findall(r'\w+', text.lower())
    # Đọc nội dung từ hai tệp tin
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        text1 = f1.read()
        text2 = f2.read()

    # Loại bỏ dấu câu và chuyển thành chữ thường
    text1 = remove_punctuation_and_lowercase(text1)
    text2 = remove_punctuation_and_lowercase(text2)

    # Tách các từ thành danh sách
    words_file1 = text1.split()
    words_file2 = text2.split()

    # Đếm số lượng từ khác nhau trong file2 so với file1
    different_words_count = 0
    words_file1_dict = {}

    # Tạo một từ điển đếm số lần xuất hiện của từ trong file1
    for word in words_file1:
        if word in words_file1_dict:
            words_file1_dict[word] += 1
        else:
            words_file1_dict[word] = 1

    # Kiểm tra từng từ trong file2 xem có xuất hiện trong file1 hay không
    for word in words_file2:
        if word not in words_file1_dict or words_file1_dict[word] == 0:
            different_words_count += 1
        else:
            words_file1_dict[word] -= 1

    WORDS = Counter(words(open(file1, 'r', encoding='utf-8').read()))
    N = sum(WORDS.values())

    return different_words_count, N / time