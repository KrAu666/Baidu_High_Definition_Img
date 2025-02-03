import json
import os
from tqdm import tqdm
import time


def creat_main(folder_name, keyword):
    number = 0
    json_number = 0
    # 指定你的JSON文件所在的文件夹路径
    json_folder_path = f'{folder_name}'

    # 指定TXT文件要保存的文件夹路径
    txt_folder_path = json_folder_path

    # 确保TXT文件的目标文件夹存在，如果不存在则创建
    if not os.path.exists(txt_folder_path):
        os.makedirs(txt_folder_path)

    # 遍历文件夹中的所有JSON文件
    for filename in tqdm(os.listdir(json_folder_path)):
        if filename.lower().endswith('.json'):
            # 构建完整的JSON文件路径
            json_file_path = os.path.join(json_folder_path, filename)
            # 构建对应的TXT文件路径
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_file_path = os.path.join(txt_folder_path, txt_filename)

            # 读取JSON文件
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                # 初始化要写入TXT文件的内容
                txt_content = ''

                if data['shapes'] == []:
                    json_number += 1

                # 遍历shapes中的每个对象
                for shape in data['shapes']:
                    if shape['label'] in keyword:
                        label = shape['label']
                        points = shape['points']

                        # 计算多边形的中心点和宽高（使用YOLO格式）
                        x_coords = [point[0] for point in points]
                        y_coords = [point[1] for point in points]

                        x_center = sum(x_coords) / len(points)
                        y_center = sum(y_coords) / len(points)

                        width = max(x_coords) - min(x_coords)
                        height = max(y_coords) - min(y_coords)

                        # 将坐标转换为相对于图像宽度和高度的比例值
                        x_center /= data['imageWidth']
                        y_center /= data['imageHeight']
                        width /= data['imageWidth']
                        height /= data['imageHeight']

                        # 写入TXT文件的内容，这里将0替换为label
                        txt_content += f"{keyword.index(label)} {x_center} {y_center} {width} {height}\n"
                    # 将内容写入TXT文件
                with open(txt_file_path, 'w') as txt_file:
                    txt_file.write(txt_content.strip())
                number += 1

    print("All JSON files have been converted to txt files.")
    print(f'有框样本数量:  {number}')
    print(f'无框样本数量:  {json_number}')
