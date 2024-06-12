import os
import pickle
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import KneserNeyInterpolated


def train_trigram_model(corpus, n, model_dir, pkl_filename):
    """
    Huấn luyện mô hình ngôn ngữ trigram và lưu trữ vào một tệp pickle.

    Parameters:
    corpus (list of str): Dữ liệu huấn luyện cho mô hình ngôn ngữ.
    n (int): Số ngữ cảnh cho mỗi từ trong mô hình.
    model_dir (str): Đường dẫn đến thư mục lưu trữ tệp pickle của mô hình.
    pkl_filename (str): Tên của tệp pickle mà mô hình sẽ được lưu vào.

    Returns:
    None
    """
    vi_model = KneserNeyInterpolated(n)

    train_data, padded_sents = padded_everygram_pipeline(n, corpus)
    vi_model.fit(train_data, padded_sents)

    with open(os.path.join(model_dir, pkl_filename + '.pkl'), 'wb') as fout:
        pickle.dump(vi_model, fout)

    print('Saved model to {0}'.format(os.path.join(model_dir, pkl_filename + '.pkl')))