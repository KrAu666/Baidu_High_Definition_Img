import json
import time
import requests
import os


# 全局变量
range_quantity = 0
download_img_quantity = 0


def build_folder(word):
    if not os.path.exists('img'):
        # 创建img文件夹
        os.mkdir('img')

    if not os.path.exists(f'./img/{word}'):
        os.mkdir(f'./img/{word}')


def download_img(quantity, download_img_quantity, word):
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
        'width': '1920',
        'height': '1080',
        'word': word,
        'pn': str(60 * quantity),
        'rn': '60',
    }

    response = requests.get('https://image.baidu.com/search/acjson', params=params, headers=headers)
    # 转化为字典
    data = json.loads(response.text)

    new_data = []
    # 筛选出没有水印的
    for i in data['data']:
        # 空字典跳过
        if i == {}:
            continue

        if i['aiEditData']['text'] != '去水印':
            new_data.append(i)

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

        response = requests.get('https://image.baidu.com/search/down', params=params, headers=headers)

        # 检查响应是否成功
        if response.status_code == 200:
            # 打开文件并保存图片
            with open(f'./img/{word}/{download_img_quantity}.jpg', 'wb') as f:
                f.write(response.content)
            print(f"第{download_img_quantity}张图片，{ObjURL}图片已成功保存！")
        else:
            print("图片下载失败，状态码：", response.status_code)

        # 下载完成一次进行一次睡眠
    return download_img_quantity


if __name__ == '__main__':
    # 需要爬取的图片数量,爬取的图片只会多于这个数不会少于这个数
    img_quantity = 500
    word = '野猪'

    # 建立对应的文件夹
    build_folder(word)

    while True:
        if download_img_quantity < img_quantity:
            # 有时候处理json的时候会出现问题，需要同一个try处理一下，只有极个别几个会出现问题
            try:
                download_img_quantity = download_img(range_quantity, download_img_quantity, word)
            except:
                print('json处理出现错误，正在下载下一页的内容')
                pass
            range_quantity += 1
        else:
            print(f'爬取结束，一共{download_img_quantity}张图片')
            break


