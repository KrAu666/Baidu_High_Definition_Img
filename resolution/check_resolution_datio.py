import cv2
import numpy as np


def get_state(path,download_img_quantity):
    # 读取图像
    image_path = path  # 替换为你的图像路径
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    if image is None:
        print("无法读取图像。请检查路径是否正确。")
    else:
        # 获取图像的高度、宽度和通道数
        height, width, channels = image.shape
        print(f"图像分辨率: {width}x{height}")

        # 检查是否符合1920x1080
        if width >= 1920 and height >= 1080:
            pass
        else:
            pass
            # 删除图片
            # os.remove(path)
            # download_img_quantity -= 1
            # print("图像分辨率不符合1920x1080的标准，已删除")
    return download_img_quantity
