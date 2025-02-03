import os
import json


# 改变当前工作目录
os.chdir('img')

# 获取 animals 文件夹下的所有文件
files = os.listdir('animals')

# 定义起始和结束的文件名对应的数字
start_num = 27324
end_num = 32393

# 允许的 label 值
allowed_labels = ['sheep', 'cat', 'cow', 'bird', 'dog', 'horse']

# 遍历所有文件
for file in files:
    # 检查文件是否为 JSON 文件
    if file.endswith('.json'):
        try:
            # 从文件名中提取数字部分
            file_num = int(os.path.splitext(file)[0])
            # 检查数字是否在指定范围内
            if start_num <= file_num <= end_num:
                # 构建完整的文件路径
                file_path = os.path.join('animals', file)
                # 打开 JSON 文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 过滤 shapes 列表，仅保留允许的 label 值对应的元素
                new_shapes = []
                for shape in data.get('shapes', []):
                    if shape['label'] in allowed_labels:
                        new_shapes.append(shape)
                data['shapes'] = new_shapes

                # 遍历 shapes 列表中的每个元素
                for shape in data.get('shapes', []):
                    # 仅当 label 的值不为 person 时，才将其修改为 sheep
                    if shape['label'] != 'person':
                        shape['label'] = 'sheep'

                # 将修改后的数据写回到文件中
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print(f"已成功修改文件: {file}")
        except ValueError:
            print(f"文件名 {file} 无法转换为有效的数字，跳过该文件。")
        except Exception as e:
            print(f"处理文件 {file} 时出现错误: {e}")