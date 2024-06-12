import random


def read_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sentences = f.readlines()
    return [sentence.strip() for sentence in sentences]


def write_sentences(file_path, sentences):
    with open(file_path, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence + '\n')


def introduce_deletion_error(sentence, rate):
    words = sentence.split()
    new_words = []
    for word in words:
        if random.random() < rate and len(word) > 1:
            new_word = word[:-1]  # Xóa một chữ cái cuối cùng
        else:
            new_word = word
        new_words.append(new_word)
    return ' '.join(new_words)


def generate_error(input_file, output_file, error_rate):
    # Đọc các câu từ file ban đầu
    sentences = read_sentences(input_file)

    # Tạo lỗi và ghi ra file mới
    error_sentences = [introduce_deletion_error(sentence, error_rate) for sentence in sentences]
    write_sentences(output_file, error_sentences)
