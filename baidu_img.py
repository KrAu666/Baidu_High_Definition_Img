import json
import time

import requests
import os
from concurrent.futures import ThreadPoolExecutor
from json_message.change_json import creat_json, update_json
from resolution.get_file_number import file_name_number
from change_file import remove_file, creat_txt, txt_new_folder, remove_json

def build_folder(word):
    if not os.path.exists('img'):
        # 创建img文件夹
        os.mkdir('img')

    if not os.path.exists(f'./img/{word}'):
        os.mkdir(f'./img/{word}')


def download_img(quantity, download_img_quantity, word, error_number, file_name):
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDEsMiwxMyw3LDYsNSwxMiw5&word=%E9%87%8E%E7%8C%AA',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'tn': 'resultjson_com',
        'width': '',
        'height': '',
        'word': word,
        'pn': str(60 * quantity),
        'rn': '60',
    }
    response = requests.get('https://image.baidu.com/search/acjson', params=params, headers=headers)
    # 转化为字典
    try:
        data = json.loads(response.text)
    except:
        return download_img_quantity, error_number

    new_data = []
    # 筛选出没有水印的
    for i in data['data']:
        # 空字典跳过
        if i == {}:
            error_number += 1
            continue
        else:
            error_number = 0

        try:
            if i['aiEditData']['text'] != '去水印':
                new_data.append(i)
        except:
            pass

    # 筛选出符合的url
    for i in new_data:
        download_img_quantity += 1
        img_url = i['thumbURL']
        ObjURL = i['replaceUrl'][0]['ObjURL']

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        }

        params = {
            'url': ObjURL,
            'thumburl': img_url,
        }

        try:
            response = requests.get('https://image.baidu.com/search/down', params=params, headers=headers, timeout=20)
        except:
            response.status_code = 404
            print(f'{word}    404')
        # 检查响应是否成功
        if response.status_code == 200:
            # 打开文件并保存图片
            path = f'./img/{file_name}/{download_img_quantity}.jpg'
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"第{download_img_quantity}张图片，{ObjURL}图片已成功保存！")

            # 筛选不符合目标分辨率的图片
            # download_img_quantity = get_state(path, download_img_quantity)
        else:
            print("图片下载失败，状态码：", response.status_code)

        # 下载完成一次进行一次睡眠
    return download_img_quantity, error_number


def download_keyword(word, key, img_quantity):
    # 建立对应的文件夹
    build_folder(word)
    for key_word in key:
        error_number = 0
        range_quantity, check = creat_json(key_word)

        # 获得接下来的range_quantity
        download_img_quantity = file_name_number(word)

        # 初始化变量
        if range_quantity is None:
            range_quantity = 1
            check = 'False'

        # 假设已经爬取完成过
        if check != 'False':
            print(f'{key_word}    已爬取结束')
            continue
        while True:
            if download_img_quantity - img_quantity < download_img_quantity:
                # 有时候处理json的时候会出现问题，需要同一个try处理一下，只有极个别几个会出现问题
                download_img_quantity, error_number = download_img(range_quantity, download_img_quantity, key_word, error_number, word)
                if download_img_quantity is None:
                    continue

                range_quantity += 1
                update_json(key_word,error_number)
                if error_number > 10:
                    print(f'{key_word}    图片已被全部爬取')
                    break
            else:
                print(f'爬取结束，一共{download_img_quantity}张图片')
                break


def img_main(words, max_threads, img_quantity, file_name):
    # 创建线程池
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # 初始化一个空列表，用于存储每个任务的 Future 对象
        futures = []
        # 遍历 words 列表中的每个元素
        for word in words:
            # 从当前 word 元素中提取文件夹名称
            folder_name = word['word']
            # 从当前 word 元素中提取关键词列表
            keywords = word['key']
            # 提交下载任务到线程池，使用 executor.submit 方法
            future = executor.submit(download_keyword, folder_name, keywords, img_quantity)
            # 将返回的 Future 对象添加到 futures 列表中
            futures.append(future)

        # 等待所有任务完成
        for future in futures:
            future.result()

    # 移动多个文件夹到新的文件夹
    remove_file.remove_new_file(words, file_name)

    # 批量处理图片
    remove_file.main(file_name)

    # 删除多余文件
    remove_file.detect_corrupted_images(file_name)


def yolo_txt_main(file_name, keyword):
    # 创建txt文件
    creat_txt.creat_main(file_name, keyword)
    # 移动至指定目录
    txt_new_folder.txt_to_folder(file_name)
    # 删除多余的json和jpg文件
    remove_json.remove_all_json(file_name)


if __name__ == '__main__':
    # 设置线程池的最大线程数量（数量为int类型）None为不限制
    max_threads = None
    # 需要爬取的图片数量,爬取的图片只会多于这个数不会少于这个数
    img_quantity = 2000

    file_name = 'animals_img'

    keyword = ['bird', "cat", "cow", "sheep", "horse", "dog", "person"]

    words = [
    ]

    print("""
    1:  爬虫模式
    2:  处理yolo数据模式
    """)
    text = input('请输入你要开始的模式')

    if text == '1':
        img_main(words, max_threads, img_quantity, file_name)
    elif text == '2':
        yolo_txt_main(file_name, keyword)
    else:
        print('请输入正确的数字')
