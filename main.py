from Data.get_data import unzip_file, read_random_files_from_directory
from Data.preprocess_data import process_data
from Train.train_model import train_trigram_model
from PostOCR.post_ocr import load_trigram_model, process_error_sentences
from Test.count_diff import count_different_words
from Generate_Error.generate_error import generate_error

zip_path = 'Train_Full.zip'
extract_path = 'Train_Full'

# Unzip dataset
# unzip_file(zip_path, extract_path)
# Lấy số file dataset
# contents = read_random_files_from_directory(extract_path, num_files=3000)
# Tiền xử lý
# corpus = process_data(contents)

model_dir = 'Model'
pkl_filename = 'Trigram (1)'
# Train model
# train_trigram_model(corpus=corpus, n=3, model_dir=model_dir, pkl_filename=pkl_filename)
# Load model
model = load_trigram_model(model_dir, pkl_filename)
#
# Generate error
input_error = 'TestData/texttrigram2.txt'
output_error = 'TestData/texttrigram2_error.txt'
error_rate = 0.3
# generate_error(input_error, output_error, error_rate)
# Thực hiện
input_file = 'TestData/texttrigram2_error.txt'
output_file = 'TestData/texttrigram2_result.txt'
file = 'TestData/texttrigram2.txt'
time = process_error_sentences(input_file=input_file, output_file=output_file, model_loaded=model)
different_words_count, time = count_different_words(file, output_file, time)
print(different_words_count)
print(str(time) + 'word/s')
