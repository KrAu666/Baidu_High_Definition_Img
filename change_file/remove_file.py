import os
import hashlib
from PIL import Image
import logging
from tqdm import tqdm
import shutil

# 改变当前工作目录
os.chdir('img')

def remove_new_file(words,file_name):
    # 创建名为file_name的文件夹
    target_folder = file_name
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历words列表中的每个字典
    for item in words:
        word = item['word']
        # 检查当前word对应的文件夹是否存在
        if os.path.exists(word):
            # 将该文件夹移动到file_name文件夹中
            shutil.move(word, os.path.join(target_folder, word))



def main(file_name):
    # 配置日志记录
    logging.basicConfig(filename='../img/image_processing.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # 定义目标文件夹
    target_folder = file_name
    # 用于计数，作为新文件名的数字部分
    count = 1

    # 去除图片元数据
    def remove_metadata(image_path):
        try:
            with Image.open(image_path) as img:
                new_img = Image.new(img.mode, img.size)
                new_img.putdata(list(img.getdata()))
                new_img.save(image_path)
        except Exception as e:
            logging.error(f"去除元数据时文件 {image_path} 出错: {e}")

    # 获取目标文件夹下所有文件数量
    total_files = sum([len(files) for _, _, files in os.walk(target_folder)])
    processed_files = 0

    # 遍历目标文件夹下的所有子文件夹
    for root, dirs, files in os.walk(target_folder):
        for file in tqdm(files):
            # 获取文件的完整路径
            old_path = os.path.join(root, file)
            try:
                # 获取文件扩展名
                file_extension = os.path.splitext(file)[1]
                # 新文件名
                new_name = f"{count}{file_extension}"
                new_path = os.path.join(target_folder, new_name)
                # 重命名并移动文件
                os.rename(old_path, new_path)
                count += 1
                # 去除元数据
                remove_metadata(new_path)
            except Exception as e:
                logging.error(f"重命名文件 {old_path} 时出错: {e}")
            processed_files += 1

    # 用于存储文件的哈希值和对应的文件路径
    hash_dict = {}
    processed_files = 0

    # 再次遍历目标文件夹
    for root, dirs, files in os.walk(target_folder):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            try:
                # 计算文件的哈希值
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                if file_hash in hash_dict:
                    # 如果哈希值已存在，说明是重复文件，删除该文件
                    print(f"发现重复文件: {file_path}，将其删除")
                    logging.info(f"发现重复文件: {file_path}，将其删除")
                    os.remove(file_path)
                else:
                    # 如果哈希值不存在，将其添加到字典中
                    hash_dict[file_hash] = file_path
            except Exception as e:
                logging.error(f"处理文件 {file_path} 时出错: {e}")
            processed_files += 1


def detect_corrupted_images(folder_path):
    # 支持的图片格式扩展名
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    # 遍历文件夹
    for root, _, files in os.walk(folder_path):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file_path)[1].lower()

            if ext in image_extensions:
                try:
                    # 尝试打开图片
                    with Image.open(file_path) as img:
                        img.verify()  # 验证文件完整性（更严格检测）
                        # 可选：检查是否包含有效数据（如尺寸是否为0）
                        if img.width == 0 or img.height == 0:
                            os.remove(file_path)
                except Exception as e:
                    os.remove(file_path)
                    print(f"损坏文件: {file_path} | 错误: {str(e)}")
