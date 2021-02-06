from selenium import webdriver  # 调用大佬的html文件
from selenium.webdriver.support import expected_conditions as EC  # 检测弹窗
import os  # 目录操作
import shutil  # 文件操作
import time  # 延时
import sys  # 强制退出程序用
import datetime


def exit_file(x):  # 退出程序
    if x == 0:
        print('咦?设置出错了,重启程序解决100%的问题!')
        sys.exit(0)


if __name__ == '__main__':
    # 初始化设置
    with open('settings.txt', 'r', encoding='utf-8') as f:  # 读入设置文件
        print_path = int(f.readline()[:-1])
        match_mod = int(f.readline()[:-1])
        match_mod2 = int(f.readline()[:-1])
        msg = f.readline()[:-1]
        compress_level = int(f.readline()[:-1])
        auto23 = int(f.readline()[:-1])
        auto4 = int(f.readline()[:-1])

    if auto23 == 1:  # 自动设置图片匹配模式和命名模式
        print('里图匹配模式:', end='')
        if match_mod == 1:
            print('等量匹配')
        elif match_mod == 2:
            print('反复使用同一张表图')
        else:
            exit_file(0)

        print('图片命名模式:', end='')
        if match_mod2 == 1:
            print('使用表图名称')
        elif match_mod2 == 2:
            print('使用前缀+序号')
            match_mod_code = input('请输入前缀(务必填写,防止长江后浪推前浪，大水冲了龙王庙):')
            match_mod_num = input('请输入起始序号:')
            if match_mod_code == '' or match_mod_num.isdigit() is False:
                exit_file(0)
            match_mod_num = int(match_mod_num)
        elif match_mod2 == 3:
            print('使用里图名称')
        else:
            exit_file(0)

    else:  # 手动设置图片匹配模式和命名模式
        match_mod = int(input('请设置里图匹配模式:\n'
                              '1.等量匹配(表图用完时停止合成)(我就是表图多,你随便合)\n'
                              '2.反复使用同一张表图(我就一张表图啦)\n'))
        if match_mod == 1:
            match_mod2 = int(input('请设置输出图片命名模式:\n'
                                   '1.使用表图名称\n'
                                   '2.使用前缀+序号\n'
                                   '3.使用里图名称\n'))
            if match_mod2 == 2:
                match_mod_code = input('请输入前缀(务必填写,防止长江后浪推前浪，大水冲了龙王庙):')
                match_mod_num = input('请输入起始序号:')
                if match_mod_code == '' or match_mod_num.isdigit() is False:
                    exit_file(0)
                match_mod_num = int(match_mod_num)
            elif match_mod2 != 1 and match_mod2 != 3:
                exit_file(0)
        elif match_mod == 2:
            match_mod2 = int(input('请设置输出图片命名模式:\n'
                                   ' .-----------\n'
                                   '2.使用前缀+序号\n'
                                   '3.使用里图名称\n'))
            if match_mod2 == 2:
                match_mod_code = input('请输入前缀(务必填写,防止长江后浪推前浪，大水冲了龙王庙):')
                match_mod_num = input('请输入起始序号:')
                if match_mod_code == '' or match_mod_num.isdigit() is False:
                    exit_file(0)
                match_mod_num = int(match_mod_num)
            elif match_mod2 != 3:
                exit_file(0)
        else:
            exit_file(0)

    if auto4 == 1:  # 自动设置水印信息
        print('水印信息:', msg)
    else:
        msg = input('请输入水印信息:')

    if compress_level == 5:  # 值为5时，需手动设置水印信息
        compress_level = int(input('请输入压缩程度,0表示自动采用系统推荐,1-4表示强制使用给定的压缩度:'))
    if compress_level < 0 or compress_level >= 5:
        exit_file(0)
    print('压缩程度:', end='')
    if compress_level == 0:
        print('采用系统推荐')
    else:
        print(compress_level)

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
    if print_path == 1:
        print('html: ', file_path,
              '\noutside_path: ', outside_path,
              '\ninside_path: ', inside_path,
              '\ngan_hao_shi_path: ', gan_hao_shi_path,
              '\ndownload_path: ', download_path,
              '\nxpath_make_tank: ', xpath_make_tank,
              '\nxpath_button: ', xpath_button,
              '\n\n',
              end='')

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

    if compress_level != 0:  # 非采用系统推荐
        input_compress.send_keys(str(compress_level))
    sentence = 'arguments[0].text = \'' + msg + '\''  # 合成水印信息
    browser.execute_script(sentence, input_msg)  # 输入水印内容

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
        compos_counter += 1
        print(compos_counter, '/', files_inside_num, ' ', end='')
        inside_complete_path = os.path.join(inside_path, i)
        img_size = os.path.getsize(inside_complete_path)  # 得到里图大小
        if compress_level == 0:  # 采用系统推荐
            if img_size < 500 * 1024:  # 里图小于0.5M
                input_compress.send_keys('1')
            elif img_size < 1000 * 1024:  # 里图小于1M
                input_compress.send_keys('2')
            elif img_size < 1500 * 1024:  # 里图小于1.5M
                input_compress.send_keys('3')
            else:  # 里图大于等于1.5M
                input_compress.send_keys('4')

        files_outside = os.listdir(outside_path)  # 获得表图
        if len(files_outside) == 0:
            break
        outside_complete_path = os.path.join(outside_path, files_outside[0])  # 获得表图文件路径
        if match_mod2 == 1:
            download_name = files_outside[0]
            download_name = download_name[:-3]
            if download_name[-1] == '.':
                download_name = download_name[:-1]
        elif match_mod2 == 2:
            download_name = match_mod_code + '_' + str(match_mod_num)
            match_mod_num += 1
        elif match_mod2 == 3:
            download_name = i[:-3]
            if download_name[-1] == '.':
                download_name = download_name[:-1]
        download_name = download_name + '.png'
        sentence = 'arguments[0].download = \'' + download_name + '\''  # 设置下载图片的名称

        input_outside.send_keys(outside_complete_path)  # 上传表图
        input_inside.send_keys(inside_complete_path)  # 上传里图
        time.sleep(0.3)  # 给系统反应时间
        input_button.click()  # 点击合成图片
        time.sleep(0.2)  # 给系统反应时间
        alert = EC.alert_is_present()(browser)  # 检查图片是否合成失败
        if alert:
            alert.accept()  # 处理弹窗
        else:
            time.sleep(0.1)  # 给系统反应时间
            browser.execute_script(sentence, output_save)  # 设置合成图名称
            time.sleep(0.1)  # 给系统反应时间
            output_save.click()
            log_msg = i + ' -> ' + download_name
            print(log_msg)
            f.write(log_msg + '\n')
            inside_used_complete_path = inside_used_path + i  # 完整的使用过的里图的路径
            shutil.move(inside_complete_path, inside_used_complete_path)  # 将使用的里图放入inside_used文件夹
            download_list.append(download_name)  # 记录下载图片名称
            if match_mod == 1:  # 等量匹配
                outside_used_complete_path = outside_used_path + files_outside[0]  # 完整的使用过的表图的路径
                shutil.move(outside_complete_path, outside_used_complete_path)
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
