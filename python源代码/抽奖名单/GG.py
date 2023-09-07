import os
import openpyxl
import PySimpleGUI as sg
import random
import _thread
import time
import csv

nameList_column = [
    [sg.Text('人员名单：')],
    [sg.Listbox(values=[], size=(20, 10), key='nameList')],
]
result_column = [
    [sg.Text('中奖记录：')],
    [sg.Multiline('', size=(48, 10), key='result', text_color='DeepPink')],
]

# 主题设置
sg.theme('SystemDefaultForReal')

# 布局设置
layout = [[sg.Text('选择参与抽奖人员名单文件:', font=('微软雅黑', 12)),
           sg.InputText('', key='_file', size=(50, 1), font=('微软雅黑', 10), enable_events=True),
           sg.FileBrowse('打开', file_types=(('Text Files', '*.xlsx'),), size=(10, 1), font=('微软雅黑', 11))],
          [sg.Frame(layout=[
              [sg.Text('本轮奖项:', font=('微软雅黑', 12)),
               sg.Combo(['特等奖', '一等奖', '二等奖', '三等奖', '四等奖', '五等奖', '六等奖'], font=('微软雅黑', 10),
                        default_value='特等奖', size=(15, 5), key='_type'),
               sg.Text('本轮人数:', font=('微软雅黑', 12)),
               sg.InputText('5', key='_num', size=(38, 1), font=('微软雅黑', 10))],
          ],
              title='抽奖设置', title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='请进行抽奖设置后再开始抽奖')],
          [sg.Multiline(size=(48, 5), font=(
              '微软雅黑', 18), text_color='Blue', key='luckyName', justification='center')],
          [sg.Column(nameList_column), sg.Column(result_column)],
          [sg.Text('操作说明:', font=('微软雅黑', 12))],
          [sg.Text(
              '①先选择参与抽奖的人员名单xlsx文件,人员名单文件包含ID和name两个字段\n②获奖名单将存在小工具所在文件夹，重置会删除历史记录文件',
              font=('微软雅黑', 10)),
           sg.Text('', font=('微软雅黑', 12), size=(5, 1)),
           sg.Button('开始抽奖', font=('微软雅黑', 12), button_color='Orange'),
           sg.Button('结束', font=('微软雅黑', 12), button_color='red'),
           sg.Button('重置', font=('微软雅黑', 12), button_color='red'), ],
          ]

# 创建窗口
window = sg.Window('抽奖小工具，作者@微信：shmily', layout,
                   font=('微软雅黑', 12), default_element_size=(50, 1))
# 初始状态
is_run = False
luckyNames = ''


def toCsv(headers, col1, col2, file):
    # 存在则追加，不存在则新建
    if os.path.exists(lucky):
        with open(lucky, 'a', encoding='utf_8_sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(zip(col1, col2))
    else:
        with open(lucky, 'w', encoding='utf_8_sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(zip(col1, col2))


def Result(window, names):
    global is_run, luckyNames
    _type = values['_type']  # 本轮奖项类型
    _num = int(values['_num'])  # 本轮人数

    while True:
        randomName = random.sample(names, k=_num)
        luckyName = '   '.join(randomName)
        window['luckyName'].update(luckyName)

        if not is_run:
            headers = ['奖项', '名单']
            toCsv(headers, [_type] * len(randomName), randomName, lucky)
            luckyNames = luckyNames + _type + ' : ' + luckyName + '\n\n'
            window['result'].update(luckyNames)
            return
        time.sleep(0.088)


def nameList(window):
    fileName = values['_file']
    try:
        wb = openpyxl.load_workbook(fileName)
        active_sheet = wb.active
        names = [cell_object.value for cell_object in list(active_sheet.columns)[1]][1:]
        ids = [cell_object.value for cell_object in list(active_sheet.columns)[0]][1:]
        names = [name + '_' + str(id_) for name, id_ in zip(names, ids)]
        window['nameList'].update(names)
        return names
    except:
        sg.popup('请选择正确格式的的人员名单文件', title='提示', )


# 事件循环
while True:
    event, values = window.read()
    if event in (None, '关闭程序'):
        break
    if event == '_file':
        nameList(window)

    if event == '开始抽奖':
        if is_run:
            sg.popup('抽奖进行中，无需重复操作......', title='提示')
            continue
        try:
            names = nameList(window)  # 人员名单
            _num = int(values['_num'])  # 本轮人数
            lucky = '中奖名单.csv'  # 中奖名单
            if os.path.exists(lucky):
                with open('中奖名单.csv', 'r', encoding='utf_8_sig') as f:
                    reader = csv.reader(f)
                    selectedNames = set([i[1] for i in reader][1:])
                names_set = set(names) - selectedNames
            else:
                names_set = set(names)
            if len(names_set) >= _num:
                is_run = True
                _thread.start_new_thread(Result, (window, names_set))
            else:
                sg.popup(
                    f'请选择正确本轮抽奖人数(当前 {len(names_set)} 个未中奖人数)', title='提示')
        except:
            sg.popup('请选择正确本轮抽奖人数(别超过总人数哦)', title='提示')
    elif event == '结束':
        is_run = False
    elif event == '重置':
        if is_run:
            sg.popup('抽奖进行中，请等待抽奖结束后重置...', title='提示')
            continue
        yes_no = sg.popup_yes_no(
            '重置会清楚历史数据，是否执行此操作？？', text_color='red', title='提示')
        if yes_no == 'Yes':
            try:
                os.remove(lucky)
                luckyNames = ''
                window['result'].update(luckyNames)
                window['luckyName'].update(luckyNames)
                sg.popup('抽奖历史记录已被重置......', title='提示')
            except:
                sg.popup('无抽奖历史记录......', title='提示')
window.close()
