import os
import pickle
import nltk
import re
import time
from nltk.tokenize import word_tokenize

from Data.preprocess_data import tokenize

nltk.download('punkt')


def load_trigram_model(model_dir, model_name):
    """
    Tải mô hình ngôn ngữ trigram từ tệp pickle.

    Parameters:
    model_dir (str): Đường dẫn đến thư mục chứa tệp pickle của mô hình.

    Returns:
    Trigram model: Mô hình ngôn ngữ trigram đã được tải.
    """
    with open(os.path.join(model_dir, model_name + '.pkl'), 'rb') as fin:
        model_loaded = pickle.load(fin)
    print("Load model")
    return model_loaded


def generate_word(word):
    letters = 'aàảãáạăằẳẵắặâầẩẫấậbceèẻẽéẹêềểễếệfghiìỉĩíịklmnoòỏõóọôồổỗốộơờởỡớợpqrstuùủũúụưừửữứựvwxyỳỷỹýỵ'
    inserts = [word + c for c in letters]  # Thêm một chữ cái mới vào cuối từ
    return set(inserts + [word])


# beam search
def beam_search(words, model, k=3):
    sequences = []
    for idx, word in enumerate(words):
        if idx == 0:
            sequences = [([x], 0.0) for x in generate_word(word) if x in model.vocab]
        else:
            all_sequences = []
            for seq in sequences:
                for next_word in generate_word(word):
                    if next_word in model.vocab:
                        current_word = seq[0][-1]
                        try:
                            previous_word = seq[0][-2]
                            score = model.logscore(next_word, [previous_word, current_word])
                        except IndexError:
                            score = model.logscore(next_word, [current_word])
                        new_seq = seq[0].copy()
                        new_seq.append(next_word)
                        all_sequences.append((new_seq, seq[1] + score))
            all_sequences = sorted(all_sequences, key=lambda x: x[1], reverse=True)
            sequences = all_sequences[:k]
    return sequences


def add_punctuation(doc1, doc2):
    # Chia văn bản thành các từ
    list1 = word_tokenize(doc1)
    list2 = word_tokenize(doc2.lower())

    # Sao chép list2 để không thay đổi danh sách gốc
    merged_list = list2.copy()

    # Regex để nhận diện ký tự không phải là chữ và số
    non_alphanumeric_regex = re.compile(r'\W')

    # Duyệt qua list1
    index_count = 0
    for index, item in enumerate(list1):
        # Nếu phần tử trong list1 là ký tự không phải là chữ và số
        if non_alphanumeric_regex.match(item):
            # Thêm ký tự này vào vị trí tương ứng trong merged_list
            merged_list.insert(index, item)
            index_count += 1
        if item.isupper():
            merged_list[index] = list2[index - index_count].upper()
        if item.istitle():
            merged_list[index] = list2[index - index_count].capitalize()

    # Merge danh sách từ thành chuỗi
    merged_sentence = ' '.join(merged_list)

    # Loại bỏ dấu cách ở trước các dấu câu
    cleaned_merged_sentence = re.sub(r'\s+([^\w\s])', r'\1', merged_sentence)

    return cleaned_merged_sentence


def combine_sentences(error_sentence, modified_sentence):
    cleaned_error_sentence = re.sub(r'[^\w\s]', '', error_sentence)
    # Tách các từ trong câu gốc và câu đã sửa
    error_words = cleaned_error_sentence.split()
    modified_words = modified_sentence.split()

    # Tìm các từ bị xóa trong câu gốc
    for i in range(len(error_words)):
        try:
            if error_words[i].lower() in modified_words[i]:
                continue
            else:
                modified_words.insert(i, error_words[i])
        except:
            modified_words.append(error_words[i])

    # Kết hợp lại các từ thành câu hoàn chỉnh
    combined_sentence = ' '.join(modified_words)
    return combined_sentence


def process_error_sentences(input_file=None, text=None, output_file=None, model_loaded=None):
    """
    Xử lý các câu lỗi từ một chuỗi văn bản hoặc từ một tệp đầu vào và ghi kết quả vào một tệp đầu ra nếu được cung cấp.

    Parameters:
    input_file (str, optional): Đường dẫn đến tệp chứa các câu lỗi. Mặc định là None.
    text (str, optional): Chuỗi văn bản chứa các câu lỗi. Mặc định là None.
    output_file (str, optional): Đường dẫn đến tệp để ghi kết quả. Mặc định là None.
    model_loaded: Mô hình đã tải sẵn để sửa lỗi câu.

    Returns:
    float: Thời gian thực thi (đơn vị: giây).
    """
    start_time = time.time()

    # Đọc văn bản từ tệp đầu vào nếu được cung cấp
    if input_file:
        with open(input_file, 'r', encoding='utf-8') as fin:
            text = fin.read()

    # Mở tệp đầu ra nếu được cung cấp
    if output_file:
        fout = open(output_file, 'w', encoding='utf-8')
    else:
        fout = None

    # Xử lý từng câu lỗi
    for sentence in text.split('\n'):
        print("Văn bản lỗi        :", sentence.strip())

        sentence_with_spaces = re.sub(r'(?<=[^\s])([^\w\s\d])', r' \1', sentence)
        sentence_with_spaces = re.sub(r'\s+', ' ', sentence_with_spaces)
        cleaned_sentence = tokenize(sentence_with_spaces, stop_words=None)
        result = beam_search(cleaned_sentence, model_loaded)

        if result:
            words = result[0][0]

            # Combine the error sentence with the list of words
            result1 = combine_sentences(sentence_with_spaces, ' '.join(words))
            result1 = add_punctuation(sentence, result1)
            # Ghi kết quả vào tệp đầu ra nếu được cung cấp
            if fout:
                fout.write(result1 + '\n')
            print("Văn bản đã sửa lỗi :", result1)

        else:
            result = sentence.strip()
            # Ghi kết quả vào tệp đầu ra nếu được cung cấp
            if fout:
                fout.write(result + '\n')
            print("Văn bản đã sửa lỗi :", result)

    # Đóng tệp đầu ra nếu đã mở
    if fout:
        fout.close()

    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time
