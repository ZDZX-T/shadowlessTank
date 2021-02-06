import os
import getpass

try:
    f = open('path.txt', 'r', encoding='')
except IOError:
    path = os.getcwd()
    print('当前目录为:', path)
    os.mkdir(path+'\\gan_hao_shi')
    os.mkdir(path+'\\inside')
    os.mkdir(path+'\\inside_used')
    os.mkdir(path+'\\outside')
    os.mkdir(path + '\\outside_used')

    f = open('log.txt', 'w', encoding='utf-8')
    f.close()

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

    f = open('settings.txt', 'w', encoding='utf-8')
    f.write('1\n')
    f.write('1\n')
    f.write('1\n')
    f.write('TK\n')
    f.write('0\n')
    f.write('0\n')
    f.write('0\n')
    f.write('1：是否输出路径调试 0不输出 1输出\n')
    f.write('2：默认图片匹配模式 1等量匹配 2多对一\n')
    f.write('3：默认图片命名模式 1使用表图名称 2使用前缀+序号 3使用里图名称\n')
    f.write('4：默认水印信息\n')
    f.write('5：默认压缩程度，5代表手动设置，0-4代表自动设置，其中0表示自动采用系统推荐的压缩度\n')
    f.write('6：是否启用2、3行的自动设置 0不启用 1启用\n')
    f.write('7：是否启用4行自动设置 0不启用 1启用\n')
    f.close()

    print('通用环境配置完毕。')
else:
    f.close()
    print('已经运行过,如果确认要重新运行请删除目录“input”、“output”、“error”、“succeed”和文件“log.txt”、“path.txt”。')
input('按回车退出程序')
