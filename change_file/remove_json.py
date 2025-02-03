import os
from tqdm import tqdm

def remove_all_json(folder_path):
    # 遍历文件夹中的所有文件
    for filename in tqdm(os.listdir(folder_path)):
        # 检查文件是否是 .json 文件
        if filename.endswith('.json') or filename.endswith('.txt') or filename.endswith('.jpg'):
            # 构建文件的完整路径
            file_path = os.path.join(folder_path, filename)
            # 删除文件
            os.remove(file_path)

    print("All json files have been deleted.")
