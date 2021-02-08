# 主要辅助进行模式设置
import os  # 目录操作
import sys  # 强制退出程序用
import getpass  # 获取用户名


def exit_file(x=0):  # 退出程序
    if x == 0:
        print('咦?设置出错了,重启程序解决100%的问题!')
        sys.exit(0)


# 自动创建环境
def auto_setup():
    # 制作目录
    path = os.getcwd()
    print('当前目录为:', path)
    os.mkdir(path + '\\gan_hao_shi')
    os.mkdir(path + '\\inside')
    os.mkdir(path + '\\inside_used')
    os.mkdir(path + '\\outside')
    os.mkdir(path + '\\outside_used')
    os.mkdir(path + '\\settings')

    # 新建log.txt
    f = open('log.txt', 'w', encoding='utf-8')
    f.close()

    # 新建path.txt
    f = open('path.txt', 'w', encoding='utf-8')
    f.write('html文件路径：\n')
    f.write(path + '\\wytk.html\n')
    f.write('五个文件夹所在路径：\n')
    f.write(path + '\\\n')
    f.write('"下载"文件夹的路径(要以\\结尾)：\n')
    user_name = getpass.getuser()  # 获取当前用户名
    string = 'C:\\Users\\' + user_name + '\\Downloads\\'
    f.write(string + '\n')
    f.write('制作坦克xpath，与合成图片xpath  照抄就行\n')
    f.write(r'/html/body/div/details[1]' + '\n')
    f.write(r'/html/body/div/details[1]/button' + '\n')
    f.close()


class DATA:
    img_match_mod = 0  # 表里图匹配模式，1等量匹配 2多对一
    img_name_mod = 0  # 图片命名模式，1使用表图名称 2使用前缀+序号 3使用里图名称
    img_name_head = ''  # 图片命名头（前缀）
    img_name_tail = 0  # 图片命名尾（序号）
    watermark_main = ''  # 固定水印信息
    watermark_num_enable = 0  # 是否开启水印中加入序号的功能， 0不开启 1开启
    compress_level = 0  # 压缩程度，0表示自动采用系统推荐的压缩度，1~4表示强制使用给定的压缩度

    # 创建新模式
    def create_new_mod(self):
        self.img_match_mod = int(input('请设置里图匹配模式:\n'
                                       '1.等量匹配(表图用完时停止合成)(我就是表图多,你随便合)\n'
                                       '2.反复使用同一张表图(我就一张表图啦)\n'))
        if self.img_match_mod == 1:
            self.img_name_mod = int(input('请设置输出图片命名模式:\n'
                                          '1.使用表图名称\n'
                                          '2.使用前缀+序号\n'
                                          '3.使用里图名称\n'))
            if self.img_name_mod == 2:
                self.img_name_head = input('请输入前缀(务必填写,防止长江后浪推前浪，大水冲了龙王庙):')
                begin_num = input('请输入起始序号:')
                if self.img_name_head == '' or begin_num.isdigit() is False:
                    exit_file(0)
                self.img_name_tail = int(begin_num)
            elif self.img_name_mod != 1 and self.img_name_mod != 3:
                exit_file(0)
        elif self.img_match_mod == 2:
            self.img_name_mod = int(input('请设置输出图片命名模式:\n'
                                          ' .-----------\n'
                                          '2.使用前缀+序号\n'
                                          '3.使用里图名称\n'))
            if self.img_name_mod == 2:
                self.img_name_head = input('请输入前缀(务必填写,防止长江后浪推前浪，大水冲了龙王庙):')
                begin_num = input('请输入起始序号:')
                if self.img_name_head == '' or begin_num.isdigit() is False:
                    exit_file(0)
                self.img_name_tail = int(begin_num)
            elif self.img_name_mod != 3:
                exit_file(0)
        else:
            exit_file(0)

        self.watermark_main = input('请输入水印信息:')
        print('是否启用造本模式？造本模式会在水印后添加序号，序号依据是里图名称。\n',
              '启用该模式应保证里图名称全部为纯数字\n',
              '在当前版本中，启用该模式会更改以下设定:\n',
              '\t·里图匹配模式强制使用模式二，即多对一\n',
              '\t·输出图片命名模式强制使用模式二，即前缀+序号\n',
              end='')
        self.watermark_num_enable = int(input('是否启用造本模式？ 0不启用 1启用  :'))
        if self.watermark_num_enable == 1:
            self.img_match_mod = 2
            if self.img_name_mod != 2:
                print('输出图片命名模式更改为:使用前缀+序号')
                self.img_name_head = input('请输入前缀(务必填写,防止长江后浪推前浪，大水冲了龙王庙):')
                begin_num = input('请输入起始序号:')
                if self.img_name_head == '' or begin_num.isdigit() is False:
                    exit_file(0)
                self.img_name_tail = int(begin_num)
            self.img_name_mod = 2
        elif self.watermark_num_enable != 0:
            exit_file()

        self.compress_level = int(input('请输入压缩程度,0表示自动采用系统推荐,1-4表示强制使用给定的压缩度:'))
        if self.compress_level < 0 or self.compress_level > 4:
            exit_file()

    # 保存新模式
    def save_new_mod(self, file_name):
        file_name = file_name + '.txt'
        f = open('settings\\' + file_name, 'w', encoding='utf-8')
        f.write(str(self.img_match_mod) + '\n')  # 1
        f.write(str(self.img_name_mod) + '\n')  # 2
        f.write(str(self.watermark_main) + '\n')  # 3
        f.write(str(self.watermark_num_enable) + '\n')  # 4
        f.write(str(self.compress_level) + '\n')  # 5
        f.write('1:表里图匹配模式，1等量匹配 2多对一\n')
        f.write('2:图片命名模式 1使用表图名称 2使用前缀+序号 3使用里图名称\n')
        f.write('3:水印信息\n')
        f.write('4:是否开启水印中加入序号的功能， 0不开启 1开启\n')
        f.write('5:压缩程度，0表示自动采用系统推荐的压缩度，1~4表示强制使用给定的压缩度\n')
        f.close()

        f = open('i2o_mod_helper.txt', 'a', encoding='utf-8')
        f.write(file_name + '\n')  # 追加一条设置记录

    # 从文件读取模式
    def read_mod(self, file_name):
        try:
            f = open('settings\\' + file_name, 'r', encoding='utf-8')
        except IOError:
            print('找不到文件', file_name)
            return 0
        else:
            self.img_match_mod = int(f.readline()[:-1])
            self.img_name_mod = int(f.readline()[:-1])
            self.watermark_main = f.readline()[:-1]
            self.watermark_num_enable = int(f.readline()[:-1])
            self.compress_level = int(f.readline()[:-1])
            return 1

    # 输出当前的设置
    def print_mod(self):
        print('\n请确认当前的设置——')
        print('表里图匹配模式:', end='')
        if self.img_match_mod == 1:
            print('等量匹配')
        elif self.img_match_mod == 2:
            print('多对一')
        else:
            print('未找到模式', self.img_match_mod, '请检查')
            exit_file()

        print('图片命名模式:', end='')
        if self.img_name_mod == 1:
            print('使用表图名称')
        elif self.img_name_mod == 2:
            print('使用前缀+序号')
            if self.img_name_head != '':  # 如果为空，则说明是载入了已有的设置，但前缀和序号还未设置，待会儿会初始化。因此这里不输出。
                print('\t前缀:', self.img_name_head)
                print('\t起始序号:', self.img_name_tail)
        elif self.img_name_mod == 3:
            print('使用里图名称')
        else:
            exit_file()

        print('水印:', self.watermark_main)
        print('造本模式:', end='')
        if self.watermark_num_enable == 0:
            print('不启用')
        elif self.watermark_num_enable == 1:
            print('启用')
        else:
            exit_file()

        print('压缩程度:', end='')
        if self.compress_level == 0:
            print('采用系统推荐')
        elif 1 <= self.compress_level <= 4:
            print('强制使用', self.compress_level)
        else:
            exit_file()

    # 设置模式
    def select_mod(self):
        try:  # 尝试打开i2o_mod_helper.txt
            f = open('path.txt', 'r', encoding='utf-8')
        except IOError:  # 找不到文件，说明环境未建立
            print('首次使用？正在初始化环境。')
            auto_setup()
            print('环境初始化完成。')
        else:
            f.close()
        settings_files_name = os.listdir('settings')  # 读取所有文件
        select = -1
        while select == -1:
            print('请选择一个模式:\n0.创建一个新模式')
            counter = 1
            for i in settings_files_name:
                print(counter, '.', i[:-4], '\n', end='')
                counter += 1
            select = int(input())
            if select < 0 or select >= counter:  # 非法数据
                select = -1
                continue
            if select == 0:
                self.create_new_mod()  # 创建新模式
                self.print_mod()  # 统一输出一遍
                cin = int(input('\n是否保存该模式？ 0不保存 1保存  :'))
                if cin == 1:
                    name = input('请为新模式起一个名字(不需要输入.txt):')
                    self.save_new_mod(file_name=name)
            else:
                name = settings_files_name[select-1]
                if self.read_mod(file_name=name) == 1:
                    self.print_mod()  # 输出一遍供确认
                    use = input('使用该设置吗？ 1使用 其他:重新选择  :')
                    if use != '1':  # 重新选择
                        select = -1
                    else:  # 使用设置，检查命名模式是否为前缀+序号
                        if self.img_name_mod == 2:
                            print('开始设置输出图片的前缀和起始序号')
                            self.img_name_head = input('请输入前缀(务必填写,防止长江后浪推前浪，大水冲了龙王庙):')
                            begin_num = input('请输入起始序号:')
                            if self.img_name_head == '' or begin_num.isdigit() is False:
                                exit_file(0)
                            self.img_name_tail = int(begin_num)
                else:
                    select = -1
