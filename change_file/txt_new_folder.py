import os
import shutil
import random
from tqdm import tqdm

def txt_to_folder(file_name):
    # 指定源文件夹路径
    source_images_folder = file_name
    source_labels_folder = file_name
    # 指定目标文件夹路径
    target_train_images_folder = r'animals/images\train'
    target_train_labels_folder = r'animals/labels\train'
    target_test_images_folder = r'animals/images\test'
    target_test_labels_folder = r'animals/labels\test'
    target_val_images_folder = r'animals/images\val'
    target_val_labels_folder = r'animals/labels\val'

    # 确保目标文件夹存在，如果不存在则创建
    for folder in [target_train_images_folder, target_train_labels_folder,
                   target_test_images_folder, target_test_labels_folder,
                   target_val_images_folder, target_val_labels_folder]:
        os.makedirs(folder, exist_ok=True)
    # 获取所有图像文件名（不包括扩展名）
    image_files = {os.path.splitext(file)[0] for file in os.listdir(source_images_folder)}
    # 获取所有标签文件名（不包括扩展名）
    label_files = {os.path.splitext(file)[0] for file in os.listdir(source_labels_folder)}

    # 确保文件名匹配
    common_files = list(image_files.intersection(label_files))


    # 如果没有共同文件，则退出脚本
    if not common_files:
        print("No common files found. Please check the file names in both folders.")
    else:
        # 打乱文件名列表以随机分配数据集
        random.shuffle(common_files)
        # 定义数据集比例
        train_ratio = 0.8
        test_ratio = 0.1
        val_ratio = 0.1
        # 计算训练集、测试集、验证集的文件数量
        total_files = len(common_files)
        train_files = int(total_files * train_ratio)
        test_files = int(total_files * test_ratio)
        val_files = total_files - train_files - test_files

        # 分配文件到不同的数据集
        for i, file_name in tqdm(enumerate(common_files), total=len(common_files), desc="分配文件中"):
            # 构建完整的文件路径
            image_file_path = os.path.join(source_images_folder, file_name + '.jpg')  # 假设图像文件为jpg格式
            label_file_path = os.path.join(source_labels_folder, file_name + '.txt')  # 假设标签文件为txt格式

            # 检查图像文件和标签文件是否同时存在
            if os.path.exists(image_file_path) and os.path.exists(label_file_path):
                # 复制图片文件
                if i < train_files:
                    target_images_folder = target_train_images_folder
                    target_labels_folder = target_train_labels_folder
                elif i < train_files + test_files:
                    target_images_folder = target_test_images_folder
                    target_labels_folder = target_test_labels_folder
                else:
                    target_images_folder = target_val_images_folder
                    target_labels_folder = target_val_labels_folder

                # 移动文件到目标文件夹
                shutil.move(image_file_path, target_images_folder)
                shutil.move(label_file_path, target_labels_folder)
            else:
                pass

        print("Datasets have been created with the following files:")
        print(f"Training set: {train_files} files")
        print(f"Testing set: {test_files} files")
        print(f"Validation set: {val_files} files")
