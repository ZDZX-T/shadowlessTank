from bs4 import BeautifulSoup  # 解析网页
from urllib import request
import time
import os
from urllib.request import urlopen

version = 'get_v1.0'  # 版本信息


def init_environment():  # 初始化环境
    f = open('memory.txt', 'w', encoding='utf-8')  # 存放之前的网址记录
    f.close()

    f = open('auto_trans.txt', 'w', encoding='utf-8')  # 设置下载完图片后是否自动调用out2inside.exe
    f.write('2\r')
    f.write('下载完图片后是否自动调用out2inside.exe?\n')
    f.write('0:不自动调用,不询问  1:自动调用  2:不自动调用，但询问')
    f.close()

    try:
        f = open('path.txt', 'r', encoding='utf-8')
    except IOError:  # 打不开，说明程序在独立文件夹内
        print('请将out2inside的path.txt复制到本文件夹内')
        input('按回车继续')
    else:  # 打开了，说明程序和out2inside.exe在一块儿
        f.close()


def get_memory():  # 获得之前的访问记录
    dic = {}
    try:
        f = open('memory.txt', 'r', encoding='utf-8')
    except IOError:  # 找不到文件，说明是第一次运行
        init_environment()
        return dic
    else:
        read = f.readline()[:-1]
        while read != '':
            dic[read] = int(f.readline()[:-1])
            read = f.readline()[:-1]
        f.close()
    return dic


def get_path():  # 获得input文件夹的路径
    f = open('path.txt', 'r', encoding='utf-8')
    path = f.readlines()[3][:-1]
    f.close()
    return path


def get_setting():  # 得到关于自动转换图片的设置
    f = open('auto_trans.txt', 'r', encoding='utf-8')
    auto = int(f.readline()[0])
    f.close()
    return auto


def get_base(u):  # 得到基础帖子网址
    if '?pn=' in u:
        i = 0
        for i in range(len(u)):
            if u[i] == '?':  # 不是基础帖子
                break
        u = u[0:i]
    return u


def write_back(dic):  # 写回访问记录
    f = open('memory.txt', 'w', encoding='utf-8')
    for i in dic.keys():
        f.write(i + '\n')
        f.write(str(dic[i]) + '\n')
    f.close()


def download_pic(u):  # 下载图片
    i = -1
    while u[i] != '/':
        i -= 1
    pic_name = u[i+1:]
    print(pic_counter, ': ', pic_name)
    request.urlretrieve(u, input_path + pic_name)
    time.sleep(0.3)


if __name__ == "__main__":
    print(version, '\r\r')  # 输出版本信息

    memory = get_memory()  # 获得之前的访问记录
    destination_path = get_path()  # 获得out2inside.exe所在文件路径
    input_path = destination_path + 'input\\'
    exe_path = destination_path + 'out2inside.exe'
    auto_trans = get_setting()  # 获得关于自动调用的设定
    while 1:
        url = input('请输入帖子网址(直接按回车则退出程序):')
        if url == '':
            break
        base_url = get_base(url)  # 得到原始信息
        if base_url in memory.keys():  # 如果曾经访问过
            begin_num = memory[base_url]  # 得到之前到达的楼层
            print('之前访问过，准备从', begin_num, '楼开始访问')
        else:
            begin_num = 0  # 之前没有访问过，则从0楼开始访问
            print('新帖，准备从1楼开始访问')
        cin = input('直接输入回车接受以上提议，否则将从输入的楼层开始访问:')
        if cin != '':
            print('收到，将从', int(cin), '楼开始访问')
            begin_num = int(cin) - 1  # 因为访问的条件是楼层数>begin_num，因此-1
        cin = input('直接输入回车访问所有人，输入任意内容只访问楼主')
        if cin == '':
            only_master = 0  # 访问所有人
        else:
            only_master = 1  # 只访问楼主
        finish_flag = 0  # 帖子遍历完成标志，此数只增不减，如果减小则说明帖子已经遍历完成
        pic_counter = 0  # 记录下载数
        page = 1  # 页数
        while page > 0:  # 将帖子循环完
            html = urlopen(base_url+'?pn='+str(page)).read().decode('utf-8')  # 打开指定帖子
            main_web = BeautifulSoup(html, 'html.parser')  # 打开指定帖子
            floors = main_web.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['l_post',
                                                                                              'l_post_bright',
                                                                                              'j_l_post',
                                                                                              'clearfix'])  # 找到所有楼层
            for floor in floors:
                if floor.find_all('div')[1].find('div') is None:  # 找不到说明不是楼主
                    is_master = 0
                else:
                    is_master = 1
                floor_num = int(floor.find_all('span', class_='tail-info')[-2].string[:-1])  # 得到楼层数
                if floor_num > finish_flag:  # 正常情况
                    finish_flag = floor_num  # 更新flag
                    if only_master == 1 and is_master == 0:  # 设置了只访问楼主而此楼不是楼主，则跳过
                        continue
                    if floor_num <= begin_num:  # 如果当前楼层小于起始楼层，则跳过
                        continue
                    print('到达', floor_num, '楼')
                    images = floor.find_all('img', class_='BDE_Image')  # 得到所有图片元素（无法区分是否为坦克图）
                    for img in images:
                        pic_counter += 1
                        download_pic(img.get('src'))
                else:  # 楼层没有变大，说明已经到达帖子末尾
                    memory[base_url] = finish_flag  # 更新记录
                    write_back(memory)  # 写回记录
                    page = -2  # 用来退出while循环
                    break  # 帖子已遍历，退出for循环
            # print('page: ', page)
            # input('调试模式，输入回车:')
            page += 1  # 翻到下一页
        trans = 0
        if auto_trans == 2:
            trans = int(input('是否进行图片转换？ 0不进行 1进行  :'))
        if auto_trans == 1 or trans == 1:
            os.system(exe_path)  # 调用out2inside.exe
