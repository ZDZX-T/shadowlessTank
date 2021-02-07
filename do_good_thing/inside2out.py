from selenium import webdriver  # 调用大佬的html文件
from selenium.webdriver.support import expected_conditions as EC  # 检测弹窗
import os  # 目录操作
import shutil  # 文件操作
import time  # 延时
import sys  # 强制退出程序用
import datetime  # 得到当前时间
import i2o_helper  # 自己的程序，帮助设置模式


def exit_file(x):  # 退出程序
    if x == 0:
        print('咦?设置出错了,重启程序解决100%的问题!')
        sys.exit(0)


if __name__ == '__main__':
    print('i2o_v1.1-beta.1', '\n')   # 输出版本信息

    # 初始化设置
    mod = i2o_helper.DATA()
    mod.select_mod()  # 选择模式

    # 初始化路径
    with open('path.txt', 'r', encoding='utf-8') as f:
        f.readline()
        line = f.readline()
        file_path = r'file://' + line[:-1]  # html文件路径

        f.readline()
        line = f.readline()
        line = line[:-1]
        outside_path = line + 'outside'
        inside_path = line + 'inside'
        gan_hao_shi_path = line + 'gan_hao_shi\\'
        outside_used_path = line + 'outside_used\\'
        inside_used_path = line + 'inside_used\\'

        f.readline()
        line = f.readline()
        download_path = line[:-1]

        f.readline()
        line = f.readline()
        xpath_make_tank = line[:-1]  # “制作坦克”
        line = f.readline()
        xpath_button = line[:-1]  # “合成图片”
    print('\ndownload_path: ', download_path, '\n\n', end='')  # 只调试download_path

    # 初始化网页
    browser = webdriver.Chrome()
    browser.get(url=file_path)
    browser.find_element_by_xpath(xpath_make_tank).click()  # 展开“制作坦克”

    input_outside = browser.find_element_by_id('ipt1')  # 定位表图上传位置
    input_inside = browser.find_element_by_id('ipt')  # 定位里图上传位置
    input_msg = browser.find_element_by_id('beizhu')  # 定位备注上传位置
    input_compress = browser.find_element_by_id('select')  # 定位表图压缩度
    input_button = browser.find_element_by_xpath(xpath_button)  # 定位“合成图片”
    output_save = browser.find_element_by_id('a1')  # 定位“保存图片”

    if mod.compress_level != 0:  # 非采用系统推荐
        input_compress.send_keys(str(mod.compress_level))  # 选择表图压缩度
    watermark_msg = 'arguments[0].value = \'' + mod.watermark_main + '\''  # 合成水印信息
    if mod.watermark_num_enable == 0:  # 不是本子模式，水印上传一遍即可
        browser.execute_script(watermark_msg, input_msg)  # 输入水印内容

    # 初始化log与合成文件名记录
    f = open('log.txt', 'a', encoding='utf-8')
    log_msg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f.write('\n')
    f.write(log_msg + '\n')
    download_list = []
    files_before = os.listdir(download_path)  # 检测冗余文件用

    # 开始合成
    files_inside = os.listdir(inside_path)  # 得到里图文件
    files_inside_num = len(files_inside)  # 里图总个数
    compos_counter = 0  # 合成计数
    for i in files_inside:  # 循环处理inside
        inside_complete_path = os.path.join(inside_path, i)
        if mod.watermark_num_enable == 1:  # 造本模式，则水印需要每次都设置
            watermark_msg = i[:-4]  # 先提取一下文件名称
            if watermark_msg[-1] == '.':  # 原文件名为.jpeg
                watermark_msg = watermark_msg[:-1]  # 再去一位
            watermark_msg = mod.watermark_main + ' ' + watermark_msg  # 合成完整水印名称
            watermark_msg = 'arguments[0].value = \'' + watermark_msg + '\''  # 合成水印js信息
            browser.execute_script(watermark_msg, input_msg)  # 输入水印内容
        img_size = os.path.getsize(inside_complete_path)  # 得到里图大小
        if mod.compress_level == 0:  # 采用系统推荐
            if img_size < 500 * 1024:  # 里图小于0.5M
                input_compress.send_keys('1')
            elif img_size < 1000 * 1024:  # 里图小于1M
                input_compress.send_keys('2')
            elif img_size < 1500 * 1024:  # 里图小于1.5M
                input_compress.send_keys('3')
            else:  # 里图大于等于1.5M
                input_compress.send_keys('4')

        files_outside = os.listdir(outside_path)  # 获得所有表图
        if len(files_outside) == 0:
            break
        outside_complete_path = os.path.join(outside_path, files_outside[0])  # 获得表图文件路径
        if mod.img_name_mod == 1:
            download_name = files_outside[0]
            download_name = download_name[:-3]
            if download_name[-1] == '.':
                download_name = download_name[:-1]
        elif mod.img_name_mod == 2:
            download_name = mod.img_name_head + '_' + str(mod.img_name_tail)
            mod.img_name_tail += 1
        elif mod.img_name_mod == 3:
            download_name = i[:-3]
            if download_name[-1] == '.':
                download_name = download_name[:-1]
        download_name = download_name + '.png'
        output_name = 'arguments[0].download = \'' + download_name + '\''  # 设置下载图片的名称

        input_outside.send_keys(outside_complete_path)  # 上传表图
        input_inside.send_keys(inside_complete_path)  # 上传里图
        time.sleep(0.3)  # 给系统反应时间
        input_button.click()  # 点击合成图片
        time.sleep(0.2)  # 给系统反应时间
        alert = EC.alert_is_present()(browser)  # 检查图片是否合成失败
        if alert:
            alert.accept()  # 处理弹窗
        else:
            compos_counter += 1
            print(compos_counter, '/', files_inside_num, ' ', end='')
            time.sleep(0.1)  # 给系统反应时间
            browser.execute_script(output_name, output_save)  # 设置合成图名称
            time.sleep(0.1)  # 给系统反应时间
            output_save.click()
            log_msg = i + ' -> ' + download_name
            print(log_msg)
            f.write(log_msg + '\n')
            inside_used_complete_path = inside_used_path + i  # 完整的使用过的里图的路径
            shutil.move(inside_complete_path, inside_used_complete_path)  # 将使用的里图放入inside_used文件夹
            download_list.append(download_name)  # 记录下载图片名称
            if mod.img_match_mod == 1:  # 等量匹配
                outside_used_complete_path = outside_used_path + files_outside[0]  # 完整的使用过的表图的路径
                shutil.move(outside_complete_path, outside_used_complete_path)  # 使用过的表图移入outside_used
        # input('调试状态,waiting for enter:')

    # 转移图片
    time.sleep(3)  # 保证下载完成
    move_counter = 0
    for i in download_list:
        download_complete_path = download_path + i  # 完整的下载的图片的路径
        gan_hao_shi_complete_path = gan_hao_shi_path + i  # 完整的输出路径
        if os.path.exists(gan_hao_shi_complete_path):
            print('\033[0;31m', '\n', 'gan_hao_shi文件夹已有 ', i, ' ,程序暂停。',
                  '\033[0m', end='')
            os.popen('explorer /select,' + gan_hao_shi_complete_path)
            input('按回车继续转移:')
        try:  # 尝试转移
            shutil.move(download_complete_path, gan_hao_shi_complete_path)
        except WindowsError:
            print('无法找到图片:', i)
        else:
            move_counter += 1
            print('[', move_counter, ']', 'move: ', i)

    # 检测冗余文件
    files_after = os.listdir(download_path)
    if len(files_before) != len(files_after):  # 有冗余
        print('监测到有冗余文件，请手动清理:')
        for i in files_after:
            if i not in files_before:
                print('\033[0;31m', i, '\033[0m', '\n', end='')
        os.startfile(download_path)  # 打开下载目录

    f.close()
    # input('调试状态，按回车结束浏览器调用')
    browser.close()
    print('共合成', compos_counter, '张图片')
