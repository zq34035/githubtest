# 执行 from package import * 时，如果包中的 __init__.py代码定义了一个名为 __all__ 的列表，就会按照列表中给出的模块名进行导入
# pip install pillow
import re

import requests
from PIL import ImageTk


# 获取页面源代码 发送POST请求
# 获取图片URL地址
# 获取图片内容 显示到窗口上

def download():
    startUrl = 'http://www.uustv.com/'
    # 获取用户输入的姓名  entry是输入标签
    name = entry.get()
    # 去空格
    name =name.strip()

    # if not name.isspace()
    if name == '':
        # 提示信息
        messagebox.showinfo('提示', '请输入名字！')
    else:
        # 模拟网页发送数据
        # 字典
        data = {
            'word': name,
            'sizes': '60',
            'fonts': 'bzcs.ttf',
            'fontcolor': '#000000'
        }

        result = requests.post(startUrl, data=data)
        # 设置编码，防止中文乱码
        result.encoding = 'utf-8'
        # 获取网页源代码
        html = result.text
        # 正则表达式
        req = '<div class="tu">﻿<img src="(.*?)"/></div>'
        # <div class="tu">&#65279;<img src="tmp/155981736332210.gif"></div>
        # <div class="tu">﻿<img src="tmp/155981736332210.gif"/></div>
        # 图片路径  时间戳是指格林威治时间1970年01月01日00时00分00秒(北京时间1970年01月01日08时00分00秒)起至现在的总秒数   tmp/152283183699750.gif
        imgPath = re.findall(req, html)
        # print(imgPath)
        # 图片完整路径
        imgUrl = startUrl + imgPath[0]
        # print(imgUrl)
        # 获取图片内容
        response = requests.get(imgUrl).content

        # with open('{}.gif'.format(name), 'wb') as f:
        # 已二进制格式打开一个文件只用于写入，如果该文件已存在则将其覆盖，如果该文件不存在，创建新文件
        f = open('{}.gif'.format(name), 'wb')
        f.write(response)
        # 显示图片
        bm = ImageTk.PhotoImage(file='{}.gif'.format(name))

        label2 = Label(root, image=bm)
        label2.bm = bm
        # columnspan 组件所跨越的列数
        label2.grid(row=2, columnspan=2)

from tkinter import *
from tkinter import messagebox

# 创建窗口
root = Tk()
# 标题
root.title('签名设计')
# 获取屏幕宽和高
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
w = 600
h =300
# 计算 x, y的位置
x = str(int(ws/2) - (w/2))
y = str(int(hs/2) - (h/2))

# 窗口大小 截图说明窗口大小
# root.geometry(str(w) + 'x' + str(h))
root.geometry('500x300')
# 标签控件 可以设置字体 大小 颜色
label = Label(root, text='签名', font=('华文行楷', 20), fg='red')
# row=0, column=0 grid 网格布局 pack place 但是不要混用
# 定位
label.grid()
# 输入框 entry 显示单行文本 Text
entry = Entry(root, font=('微软雅黑', 25))
# row 行 column 列 pack place
entry.grid(row=0, column=1)

# 点击按钮
button = Button(root, text='设计签名', font=('微软雅黑', 20), command=download)
# button['width'] = 10
# button['height'] = 1
# 你可以使用sticky选项去指定对齐方式 E,W
button.grid(row=1, column=1)
# 消息循环
root.mainloop()