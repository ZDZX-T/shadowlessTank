# 本文件用来辅助判断一个图片是否可能为坦克
from PIL import Image


def is_tank(path):
    threshold_white = 190
    threshold_black = 40
    try:
        img = Image.open(path)
    except Exception:  # 曾经是IOError
        return 0  # 解码不了直接返回0
    try:
        img_rgb = img.convert('RGB')
    except Exception:  # 转换不了也直接返回0
        return 0
    black = 0  # 是否查找到了黑色
    white = 0  # 是否查找到了白色
    for j in range(12, 15):
        for i in range(0, 28):
            r, g, b = img_rgb.getpixel((i, j))
            if r >= threshold_white and g >= threshold_white and b >= threshold_white:  # 可以判断为白色了
                white = 1
            elif r <= threshold_black and g <= threshold_black and b <= threshold_black:  # 可以判断为黑色了
                black = 1
            if white == 1 and black == 1:
                return 1
    return 0


if __name__ == '__main__':  # 测试用
    while 1:
        img_path = input('路径:')
        print(is_tank(img_path))
