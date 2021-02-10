from selenium import webdriver  # 调用大佬的html文件
from selenium.webdriver.support import expected_conditions as EC  # 检测弹窗
import os  # 目录操作
import shutil  # 文件操作
import time  # 延时
import auto_setup  # 自己的程序，检查环境是否完整
from pathlib import Path  # 检查文件是否存在
import tk_helper  # 先行判断一张图片是否为坦克
import sys  # 强制退出程序用
import traceback  # 输出错误信息


print('o2i_v1.2.3', '\n')  # 输出版本信息
print('提示:因兼容性问题，部分输出语句会以\" b\' \"开头，以\" \' \"结尾。且本程序被其他程序调用时，中文部分可能变为其他字符。')
print('Tip: due to compatibility problems, some output statements will start with \" b\' \" and end with \" \' \". \n'
      'And when this program is called by other programs, the Chinese part may become other characters.')

auto_setup.check_environment()  # 检查各种路径各种文件是否存在

# 初始化路径
with open('path.txt', 'r', encoding='utf-8') as f:
    f.readline()
    line = f.readline()[:-1]
    file_path = r'file://' + line  # html文件路径

    f.readline()
    line = f.readline()[:-1]
    input_path = line + 'input\\'
    output_path = line + 'output\\'
    succeed_path = line + 'succeed\\'
    error_path = line + 'error\\'

    f.readline()
    download_path = f.readline()[:-1]  # 下载路径

    f.readline()
    skip = f.readline()[0]  # 跳过转移

    f.readline()
    auto_dolls = int(f.readline()[0])  # 是否自动解套娃

    f.readline()
    test_tank = int(f.readline()[0])  # 是否提前判断是否为坦克
print('\ndownload_path:\t', download_path, '\n\n', end='')  # 只调试download_path

# 初始化是否自动解套娃的设置 是否提前判断是否为坦克的设置
if auto_dolls == 2:
    auto_dolls = int(input('本次转换是否尝试解套娃？ 0否 1是  :'))
if test_tank == 2:
    test_tank = int(input('本次转换是否提前判断是否为坦克？ 0否 1是  :'))

# 初始化网页
if not Path(file_path[7:]).exists():  # 检查wytk.html是否存在
    print('无法打开wytk.html，确认其是否在文件夹内')
    input('')
    sys.exit(0)
try:  # 尝试打开浏览器
    browser = webdriver.Chrome()
except Exception:
    print('无法打开Chrome浏览器，可能是没有设置系统Path，也可能是Chrome根目录下没有chromedriver.exe')
    print('无法打开Chrome浏览器，可能是没有设置系统Path，也可能是Chrome根目录下没有chromedriver.exe')
    print('具体信息:')
    traceback.print_exc()
    input('')
    sys.exit(0)
browser.get(url=file_path)
xpath_unfold = r'/html/body/div/details[2]'  # '坦克现形'所在位置
browser.find_element_by_xpath(xpath_unfold).click()  # 展开“坦克现形”
img_pos = browser.find_element_by_id('a2')  # 下载图片

log = open('log.txt', 'a', encoding='utf-8')  # 写入转换记录
files_before = os.listdir(download_path)  # 与之后的目录文件做对比,防止重复下载产生冗余文件

# 循环处理input文件夹下的文件
files = os.listdir(input_path)
files_num = len(files)  # 处理的图片个数
files_num_origin = files_num  # 初始状态input下图片个数
file_counter = 1  # 记录正在处理的图片编号
download_counter = 0  # 记录下载个数
img_dict = {}  # 存储下载记录与对应关系
error_list = []  # 记录失败的信息，在阶段结束后统一再次输出
succeed_list = {}  # 记录成功的信息，为解套娃做准备
now_mod = 1  # 标志现在正在干什么，1正常解图片，2+进入解套娃模式，0可以退出了
while now_mod > 0:
    succeed_list.clear()
    for i in files:
        print(str(file_counter), '/', str(files_num), ' ', end='')
        file_counter += 1

        if now_mod == 1:
            rel_path = os.path.join(input_path, i)  # 合成图片路径，没有进入套娃模式时图片来自input
        else:
            rel_path = os.path.join(download_path, i)  # 合成图片路径，进入套娃模式时图片来自download
        if test_tank == 1 and tk_helper.is_tank(rel_path) == 0:  # 开启了提前验证坦克，且提前验证结果为 非坦克
            print(str(i).encode('utf-8'), '被提前判断为可能不是坦克，如果其位于input，那么其将停留在input，本次转换完成后请人工核验。'
                                          '如需强制转换请到path.txt更改设置')
            continue
        browser.find_element_by_id('ipt2').send_keys(rel_path)  # 上传图片
        time.sleep(0.3)  # 防止来不及弹出alert
        alert = EC.alert_is_present()(browser)  # 检查图片是否读取失败
        if alert:  # 图片读取失败
            print(str(i).encode('utf-8'), ' can\'t open\n', end='')  # 输出失败文件名
            alert.accept()  # 处理弹出框
            if now_mod == 1:  # 来源是原图才做下面的事情
                error_list.append(i)  # 记录失败文件名
                shutil.move(input_path + i, error_path + i)  # 从input文件夹移入error
        else:  # 图片读取成功
            download_counter += 1
            img_name = img_pos.get_attribute('download')
            if now_mod == 1:  # 第一层干的事
                img_dict[img_name] = i  # 关联输出图片与输入图片
                message = i + ' -> ' + img_name  # 合并输出信息
                shutil.move(input_path + i, succeed_path + i)  # 从input文件夹移入succeed
            else:  # 解套娃干的事
                img_dict[img_name] = img_dict[i]  # 关联输出图片与输入图片的信息。不管是孙子还是曾孙，他祖上都一样
                message = img_dict[img_name] + ' -' + str(now_mod) + '> ' + img_name
            succeed_list[img_name] = 1  # 不管now_mod是啥，本轮的成功文件表总是要记录的
            print(message.encode('utf-8'))
            log.write(message + '\n')  # 将转换信息写入log，方便以后查找对应关系
            img_pos.click()  # 点击下载
    if now_mod == 1:
        download_counter_origin = download_counter  # 第一轮的转换信息
    if auto_dolls == 0:  # 不是解套娃模式，直接退出
        now_mod = 0
    elif len(succeed_list.keys()) != 0:  # 有成功的，则继续解套娃
        now_mod += 1
        files = list(succeed_list.keys())  # 更新输入文件的列表
        files_num = len(files)  # input下图片个数
        file_counter = 1  # 记录正在处理的图片编号
        print('两秒后开始尝试解第', now_mod, '层套娃')
        time.sleep(2)  # 不管三七二十一，等它两秒先
    else:
        now_mod = 0  # 没有成功的了，可以退出了

print('图片转换完成，切勿手动关闭，两秒后浏览器自动关闭')
time.sleep(2)
browser.close()  # 关闭浏览器
log.close()  # 关闭log文件
print('\n', end='')  # 转换阶段完成，打个空行

# 重新输出无法打开的文件名
if len(error_list) != 0:
    print('共有{}个图片未打开,名称分别为:'.format(len(error_list)))
    for i in error_list:
        print('\t', i)
    print('\n', end='')  # 报错阶段完成，打个空行

move_counter = 0  # 转移个数
if skip == '0':
    for i in img_dict.keys():  # 转移
        try:
            shutil.move(download_path + i, output_path + i)  # 尝试转移文件
        except WindowsError:
            if Path(succeed_path + img_dict[i]).exists():
                shutil.move(succeed_path + img_dict[i], input_path + img_dict[i])
            print('找不到文件\"', str(i).encode('utf-8'), '\",原始文件\"', img_dict[i].encode('utf-8'), '\"已放回input文件夹')
        else:
            move_counter += 1
            print('[', move_counter, ']', 'move: ', str(i).encode('utf-8'))
    print('\n', end='')  # 转移阶段完成，打个空行

    files_after = os.listdir(download_path)
    if len(files_before) != len(files_after):  # 有冗余文件存在
        print('检测到有冗余文件,请手动清理。')
        for i in files_after:
            if i not in files_before:
                print('\t', str(i).encode('utf-8'))
        os.startfile(download_path)  # 打开下载目录
        print('\n', end='')  # 报错阶段完成，打个空行

print('input共{}个图片,其中{}个可读取,{}个锤子'.format(files_num_origin, download_counter_origin,
                                          files_num_origin - download_counter_origin), end='')
if skip == '0':
    print(',净输出{}张图片'.format(move_counter))

# 处理input内的剩余文件
files = os.listdir(input_path)
if len(files) != 0:
    print('input文件夹内仍有剩余文件，两秒后自动打开input文件夹')
    time.sleep(2)
    os.startfile(input_path)
    print('请进行必要的处理，处理后请选择:')
    todo = int(input('是否将现存于input内的文件移入error？ 0否 1是  :'))
    if todo == 1:
        for i in files:
            shutil.move(input_path + i, error_path + i)
