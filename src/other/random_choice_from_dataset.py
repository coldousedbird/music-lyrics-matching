import os
import random
import shutil
import glob



# Путь к исходной папке
source_dir = '../../data/all_songs'

# Путь к папке назначения
dest_dir = '../../data/short_dataset'

# Количество файлов, которые нужно скопировать
num_files = 100

# Получить список всех файлов в исходной папке
#files = os.listdir(source_dir)
files = glob.glob(source_dir + '/*.mp3')

# Выбрать случайные файлы
selected_files = random.sample(files, num_files)
def extract_filename(path):
    file = path.rsplit("/", 1)
    return file[-1] if len(path) > 1 else path

selected_files = map(extract_filename, selected_files)
    

# Скопировать выбранные файлы в папку назначения
for file in selected_files:
    src_path = os.path.join(source_dir, file)
    dst_path = os.path.join(dest_dir, file)
    shutil.copy2(src_path, dst_path)
    print(f'Copied from {src_path} to {dst_path}')

    src_path = src_path[0:-4]+".lrc"
    dst_path = dst_path[0:-4]+".lrc"
    shutil.copy2(src_path, dst_path)
    print(f'Copied from {src_path} to {dst_path}')