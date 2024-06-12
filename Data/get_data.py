import os
import random
import zipfile

import os
import random
import zipfile

def unzip_file(zip_path, extract_path):
    """
    Giải nén tệp zip vào thư mục đích.

    Parameters:
    zip_path (str): Đường dẫn đến tệp zip.
    extract_path (str): Đường dẫn để giải nén tệp zip.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def read_random_files_from_directory(directory_path, num_files=3000, encoding='UTF-16'):
    """
    Chọn ngẫu nhiên các tệp từ thư mục và đọc nội dung của chúng.

    Parameters:
    directory_path (str): Đường dẫn đến thư mục chứa các tệp.
    num_files (int): Số lượng tệp cần chọn ngẫu nhiên. Mặc định là 3000.
    encoding (str): Mã hóa của các tệp văn bản. Mặc định là 'UTF-16'.

    Returns:
    list: Danh sách chứa nội dung của các tệp đã chọn.
    """
    file_paths = []

    # Duyệt qua tất cả các file trong thư mục và thu thập tên file
    for dirname, _, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            file_paths.append(file_path)

    # Chọn ngẫu nhiên các file từ danh sách các file đã thu thập
    selected_files = random.sample(file_paths, num_files)

    full = []

    # Đọc nội dung của các file đã chọn và lưu vào danh sách `full`
    for file_path in selected_files:
        with open(file_path, 'r', encoding=encoding) as f:
            print(file_path)
            content = f.read()
            full.append(content)

    return full