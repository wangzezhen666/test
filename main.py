# coding : UTF-8
from tkinter import *
import urllib.request
import gzip
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from tkinter import messagebox





def main():
    # 输入窗口
    root = Tk()
    root.title('天气预报')  # 窗口标题
    Label(root, text='请输入城市').grid(row=0, column=0)  # 设置标签并调整位置
    enter = Entry(root)  # 输入框
    enter.grid(row=0, column=1, padx=20, pady=20)  # 调整位置
    enter.delete(0, END)  # 清空输入框
    enter.insert(0, '')  # 设置默认文本
    # enter_text = enter.get()#获取输入框的内容

    running = 1

    def get_weather_data():  # 获取网站数据
        city_name = enter.get()  # 获取输入框的内容
        url1 = 'http://wthrcdn.etouch.cn/weather_mini?city='
        url2 = url1 + urllib.parse.quote(city_name)
        # url2 = 'http://wthrcdn.etouch.cn/weather_mini?citykey=101010100'
        # 网址1只需要输入城市名，网址2需要输入城市代码
        # print(url1)
        # 用于打开一个远程的url连接,并且向这个连接发出请求,获取响应结果
        weather_data = urllib.request.urlopen(url2).read()
        print('Response响应结果数据格式：')
        print(weather_data)
        # 读取网页数据,以字符串的字节格式解压缩压缩的字符串
        print('按utf-8编码读取网页数据，并解压被压缩的字符串：')
        weather_data = gzip.decompress(weather_data).decode('utf-8')
        print(weather_data)
        # 解压网页数据
        weather_dict = json.loads(weather_data)
        print(' 将json数据转换为dict数据:')
        print(weather_dict)
        # 将json数据转换为字符串数据
        # weather_str = str(weather_data)
        # print(weather_str)
        # 将json数据转换为dict数据
        if weather_dict.get('desc') == 'invilad-citykey':
            print(messagebox.askokcancel("错误", "你输入的城市名有误，或者天气中心未收录你所在城市"))
        else:
            show_data(weather_dict, city_name)
            show_pic(weather_dict, city_name)

    def show_pic(weather_str, city_name):
        forecast1 = weather_str.get('data').get('forecast')
        rows = []
        for i in range(5):
            rows.append(forecast1[i].get('date'))
        print(rows)
        high_nums = []
        for i in range(5):
            high_str = forecast1[i].get('high')
            high_numb = int(high_str[3:5])
            high_nums.append(high_numb)
        low_nums = []
        for i in range(5):
            low_str = forecast1[i].get('low')
            low_numb = int(low_str[3:5])
            low_nums.append(low_numb)
        plt.ylabel('温度 / ℃')
        plt.xlabel('日期')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        my_font = fm.FontProperties(fname=r"C:\Windows\Fonts\simkai.ttf")
        ln1, = plt.plot(rows, high_nums, color='red',  linewidth=2.0, linestyle='--',)
        ln2, = plt.plot(rows, low_nums, color='blue',  linewidth=3.0, linestyle='-.')
        plt.title("未来一周气温预测折线图", fontproperties=my_font)  # 设置标题及字体
        plt.legend(handles=[ln1, ln2], labels=['最高气温', '最低气温'], prop=my_font)
        ax = plt.gca()
        ax.spines['right'].set_color('none')  # right边框属性设置为none 不显示
        ax.spines['top'].set_color('none')  # top边框属性设置为none 不显示
        # plt.figure(figsize=[10, 6])
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        # p1 = plt.subplot(221)
        # plt.bar(rows, high_nums, width=0.3, color='green')
        # plt.ylabel("最高气温", rotation=90)
        # plt.xticks(list(rows), rotation=-60, size=8)
        # for a, b in zip(list(rows), list(high_nums)):
            # plt.text(a, b, b, ha='center', va='bottom', size=6)
        # plt.sca(p1)
        plt.show()

    def show_data(weather_dict, city_name):  # 显示数据
        forecast = weather_dict.get('data').get('forecast')  # 获取数据块
        root1 = Tk()  # 副窗口
        root1.geometry('650x280')  # 修改窗口大小
        root1.title(city_name + '天气状况')  # 副窗口标题

        # 设置日期列表
        for i in range(5):  # 将每一天的数据放入列表中
            LANGS = [(forecast[i].get('date'), '日期'),
                     (forecast[i].get('fengxiang'), '风向'),
                     (str(forecast[i].get('fengli')), '风级'),
                     (forecast[i].get('high'), '最高温'),
                     (forecast[i].get('low'), '最低温'),
                     (forecast[i].get('type'), '天气')]
            group = LabelFrame(root1, text='天气状况', padx=0, pady=0)  # 框架
            group.pack(padx=11, pady=0, side=LEFT)  # 放置框架
            for lang, value in LANGS:  # 将数据放入框架中
                c = Label(group, text=value + ': ' + lang)
                c.pack(anchor=W)
        Label(root1, text='今日' + weather_dict.get('data').get('ganmao'),
              fg='green').place(x=40, y=20, height=40)  # 温馨提示
        Label(root1, text="StarMan: 49star.com", fg="green", bg="yellow").place(x=10, y=255, width=125,
                                                                                height=20)  # 作者网站
        Button(root1, text='确认并退出', width=10, command=root1.quit).place(x=500, y=230, width=80, height=40)  # 退出按钮
        root1.mainloop()

    # 布置按键
    Button(root, text="确认", width=10, command=get_weather_data) \
        .grid(row=3, column=0, sticky=W, padx=10, pady=5)
    Button(root, text='退出', width=10, command=root.quit) \
        .grid(row=3, column=1, sticky=E, padx=10, pady=5)
    if running == 1:
        root.mainloop()


if __name__ == '__main__':
    main()




