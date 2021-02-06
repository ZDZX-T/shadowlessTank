import os
import getpass

try:
    f = open('path.txt', 'r', encoding='')
except IOError:
    path = os.getcwd()
    print('当前目录为:', path)
    os.mkdir(path+'\\input')
    os.mkdir(path+'\\output')
    os.mkdir(path+'\\error')
    os.mkdir(path+'\\succeed')
    f = open('log.txt', 'w', encoding='utf-8')
    f.close()
    f = open('path.txt', 'w', encoding='utf-8')
    f.write('html文件路径：\n')
    f.write(path + '\\wytk.html\n')
    f.write('input、output、succeed、error文件夹所在路径：\n')
    f.write(path + '\\\n')
    f.write('"下载"文件夹的路径(要以\\结尾)：\n')
    user_name = getpass.getuser()  # 获取当前用户名
    string = 'C:\\Users\\' + user_name + '\\Downloads\\'
    f.write(string + '\n')
    f.write('是否跳过转移下载文件的环节 0否 1是\n')
    f.write('0\n')
    f.close()
    print('通用环境配置完毕。')
else:
    f.close()
    print('已经运行过,如果确认要重新运行请删除目录“input”、“output”、“error”、“succeed”和文件“log.txt”、“path.txt”。')
input('按回车退出程序')
