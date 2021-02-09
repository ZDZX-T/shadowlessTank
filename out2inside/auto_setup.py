import os
import getpass
from pathlib import Path


def check_environment():
    now_path = os.getcwd()
    print('当前目录为:', now_path)

    path = Path(os.path.join(now_path, 'input'))  # 检测input文件夹是否存在
    if not path.exists():
        os.mkdir(path)

    path = Path(os.path.join(now_path, 'output'))  # 检测output文件夹是否存在
    if not path.exists():
        os.mkdir(path)

    path = Path(os.path.join(now_path, 'error'))  # 检测error文件夹是否存在
    if not path.exists():
        os.mkdir(path)

    path = Path(os.path.join(now_path, 'succeed'))  # 检测succeed文件夹是否存在
    if not path.exists():
        os.mkdir(path)

    path = Path(os.path.join(now_path, 'log.txt'))  # 检测log.txt是否存在
    if not path.exists():
        f = open('log.txt', 'w', encoding='utf-8')
        f.close()

    path = Path(os.path.join(now_path, 'path.txt'))  # 检测path.txt是否存在
    renew = 0  # 更新path标志
    if not path.exists():
        renew = 1
    else:
        f = open('path.txt', 'r', encoding='utf-8')
        lines_num = len(f.readlines())
        # print('总行数:', lines_num)
        if lines_num < 10:  # 小于说明不是最新的版本
            renew = 1
        f.close()
    if renew == 1:
        f = open('path.txt', 'w', encoding='utf-8')
        f.write('html文件路径：\n')
        f.write(now_path + '\\wytk.html\n')
        f.write('input、output、succeed、error文件夹所在路径：\n')
        f.write(now_path + '\\\n')
        f.write('"下载"文件夹的路径(要以\\结尾)：\n')
        user_name = getpass.getuser()  # 获取当前用户名
        string = 'C:\\Users\\' + user_name + '\\Downloads\\'
        f.write(string + '\n')
        f.write('是否跳过转移下载文件的环节 0否 1是\n')
        f.write('0\n')
        f.write('是否自动尝试解套娃  0不自动解套娃，不询问  1自动解套娃  2不自动解套娃，但询问\n')
        f.write('2\n')
        f.close()
        print('“下载”文件夹的路径被更新，请检查是否正确')
