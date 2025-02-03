import json
import os
import threading

# 定义 JSON 文件路径
json_file = './data.json'
lock = threading.Lock()

def creat_json(word):
    # 定义变量
    range_quantity = 1

    with lock:
        # 检查 JSON 文件是否存在
        if os.path.exists(json_file):
            # 读取现有的数据
            with open(json_file, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    # 如果文件内容为空或格式错误，初始化为空列表
                    data = []

        else:
            # 如果文件不存在，初始化为空列表
            data = []

        # 初始化变量以存储返回的 range_quantity
        returned_range_quantity = None
        check = None

        # 检查是否已经存在指定的 word
        for entry in data:
            if entry.get('word') == word:
                returned_range_quantity = entry.get('range_quantity')
                check = entry.get('check')
                break

        # 如果不存在，则添加新的条目
        if returned_range_quantity is None:
            new_entry = {
                'word': word,
                'range_quantity': range_quantity,
                'check': "False"
            }
            data.append(new_entry)
        else:
            pass

        # 将更新后的数据写回 JSON 文件
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return returned_range_quantity, check


def update_json(word,error_number):
    with lock:
        # 检查 JSON 文件是否存在
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        # 遍历数据以查找并更新 word
        for entry in data:
            if entry.get('word') == word:
                entry['range_quantity'] += 1
                updated_range_quantity = entry['range_quantity']
                if error_number > 10:
                    entry['check'] = "Ture"
                    print(f'{word}    已爬取结束')
                print(f"更新条目: word = '{word}', new range_quantity = {updated_range_quantity}")
                break

        # 将更新后的数据写回 JSON 文件
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return updated_range_quantity
