import re
import nltk
import string
import os
from nltk import word_tokenize
from tqdm import tqdm

nltk.download('punkt')


def load_stopwords():
    """
    Load stop words từ một danh sách tĩnh.

    Returns:
    set: Tập hợp các stop words.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stopwords_file = os.path.join(script_dir, "..", "Dataset", "Stopword", "stopwords.txt")
    with open(stopwords_file, "r", encoding="utf-8") as f:
        stop_words = set(f.read().splitlines())
    return stop_words


def remove_stopwords(tokens, stop_words):
    """
    Loại bỏ stop words từ danh sách tokens.

    Parameters:
    tokens (list): Danh sách tokens.
    stop_words (set): Tập hợp các stop words.

    Returns:
    list: Danh sách tokens đã loại bỏ stop words.
    """
    return [word for word in tokens if word not in stop_words]


def tokenize(doc, stop_words):
    """
    Tokenize văn bản và loại bỏ stop words.

    Parameters:
    doc (str): Văn bản đầu vào.
    stop_words (set): Tập hợp các stop words.

    Returns:
    list: Danh sách tokens đã loại bỏ stop words.
    """
    if stop_words is None:
        stop_words = load_stopwords()
    tokens = word_tokenize(doc.lower())
    table = str.maketrans('', '', string.punctuation.replace("_", ""))
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    tokens = remove_stopwords(tokens, stop_words)
    return tokens


def process_data(full):
    """
    Xử lý dữ liệu văn bản, token hóa và loại bỏ stop words.

    Parameters:
    full (list): Danh sách các văn bản.

    Returns:
    list: Danh sách các câu đã được token hóa và loại bỏ stop words.
    """
    stop_words = load_stopwords()

    full_data = ". ".join(full)
    full_data = full_data.replace("\n", ". ")

    corpus = []
    sents = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', full_data)

    for sent in tqdm(sents):
        corpus.append(tokenize(sent, stop_words))

    return corpus


# Sử dụng các hàm này
# if __name__ == "__main__":
#     full = ["Đây là văn bản mẫu số 1.", "Văn bản mẫu số 2 đang được xử lý."]
#
#     corpus = process_data(full)
#     print(corpus)
