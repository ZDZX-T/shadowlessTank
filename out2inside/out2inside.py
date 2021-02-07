from selenium import webdriver  # 调用大佬的html文件
from selenium.webdriver.support import expected_conditions as EC  # 检测弹窗
import os  # 目录操作
import shutil  # 文件操作
import time  # 延时

print('o2i_v1.0-beta.2', '\n')  # 输出版本信息

# 初始化路径
with open('path.txt', 'r', encoding='utf-8') as f:
    f.readline()
    line = f.readline()[:-1]
    file_path = r'file://' + line  # html文件路径

    f.readline()
    line = f.readline()[:-1]
    input_path = line + 'input'
    output_path = line + 'output\\'
    succeed_path = line + 'succeed\\'
    error_path = line + 'error\\'

    f.readline()
    line = f.readline()[:-1]
    download_path = line

    f.readline()
    line = f.readline()
    skip = line[0]
print('\ndownload_path:\t', download_path, '\n\n', end='')  # 只调试download_path

# 初始化网页
browser = webdriver.Chrome()
browser.get(url=file_path)
xpath_unfold = r'/html/body/div/details[2]'  # '坦克现形'所在位置
browser.find_element_by_xpath(xpath_unfold).click()  # 展开“坦克现形”

log = open('log.txt', 'a')  # 写入转换记录
files_before = os.listdir(download_path)  # 与之后的目录文件做对比,防止重复下载产生冗余文件

# 循环处理input文件夹下的文件
files = os.listdir(input_path)
files_num = len(files)  # input下图片个数
file_counter = 1  # 记录正在处理的图片编号
download_counter = 0  # 记录下载个数
img_dict = {}  # 存储下载记录与对应关系
error_list = []  # 记录失败的信息，在阶段结束后统一再次输出
for i in files:
    print(str(file_counter), '/', str(files_num), ' ', end='')
    file_counter += 1

    rel_path = os.path.join(input_path, i)  # 合成图片路径
    browser.find_element_by_id('ipt2').send_keys(rel_path)  # 上传图片
    time.sleep(0.2)  # 防止来不及弹出alert
    alert = EC.alert_is_present()(browser)  # 检查图片是否读取失败
    if alert:  # 图片读取失败
        print(i, ' can\'t open\n', end='')  # 输出失败文件名
        error_list.append(i)  # 记录失败文件名
        alert.accept()  # 处理弹出框
        shutil.move(input_path+'\\'+i, error_path+i)  # 从input文件夹移入error
    else:  # 图片读取成功
        download_counter += 1
        img_pos = browser.find_element_by_id('a2')
        img_name = img_pos.get_attribute('download')
        img_dict[img_name] = i  # 关联输出图片与输入图片
        message = i + ' -> ' + img_name  # 合并输出信息
        print(message)
        log.write(message + '\n')  # 将转换信息写入log，方便以后查找对应关系
        img_pos.click()  # 点击下载
        shutil.move(input_path+'\\'+i, succeed_path+i)  # 从input文件夹移入succeed
time.sleep(3)
browser.close()  # 关闭浏览器
log.close()  # 关闭log文件
print('\n', end='')  # 转换阶段完成，打个空行

# 重新输出无法打开的文件名
if len(error_list) != 0:
    print('共有{}个图片无法打开,名称分别为:'.format(files_num - download_counter))
    for i in error_list:
        print('\t', i)
    print('\n', end='')  # 报错阶段完成，打个空行

if skip == '0':
    move_counter = 0  # 转移个数
    for i in img_dict.keys():  # 转移
        try:
            shutil.move(download_path + i, output_path + i)  # 尝试转移文件
        except WindowsError:
            shutil.move(succeed_path+img_dict[i], input_path+'\\'+img_dict[i])
            print('未找到\"', i, '\",对应文件\"', img_dict[i], '\"已放回input文件夹')
        else:
            move_counter += 1
            print('[', move_counter, ']', 'move: ', i)
    print('\n', end='')  # 转移阶段完成，打个空行

    files_after = os.listdir(download_path)
    if len(files_before) != len(files_after):  # 有冗余文件存在
        print('检测到有冗余文件,请手动清理。')
        for i in files_after:
            if i not in files_before:
                print('\t', i)
        os.startfile(download_path)  # 打开下载目录
        print('\n', end='')  # 报错阶段完成，打个空行

print('input共{}个图片,其中{}个可读取,{}个锤子'.format(files_num, download_counter, files_num-download_counter), end='')
if skip == '0':
    print(',净输出{}张图片'.format(move_counter))
