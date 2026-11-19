'''自己的首页'''
import streamlit as st
import pandas as pd
from PIL import Image
import time
import os
import platform

page = st.sidebar.radio('我的首页',['首页','下载','音乐','图片处理','我的私人词典','留言区','调查','网页导航','时间','关于'])

PCL_file = "./PCL.exe"
haigui2_file = 'https://static.codemao.cn/turtle/client/release/%E6%B5%B7%E9%BE%9F%E7%BC%96%E8%BE%91%E5%99%A82-x64-2.4.0.exe'
classin64_file = 'https://download.eeo.cn/client/classin_win_install_5.1.1.54_x64.exe'
todesk_file = './ToDesk(远程桌面) 安装包.exe'

help_page12_list = ['操作完成']

def img_change(img, rc, gc, bc):
    '''图片处理'''
    width, height = img.size
    img_array = img.load()
    for x in range(width):
        for y in range(height):
            # 获取RGB值
            r = img_array[x, y][rc]
            g = img_array[x, y][gc]
            b = img_array[x, y][bc]
            img_array[x, y] = (r, g, b)
    return img
def help_page9(name,URL):
    st.write(name)
    st.write(URL)
    st.text('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')

def page_home():
    st.write(':orange[:sunglasses: Python创赛营根据地 :sunglasses]')
    st.write(':red[ 欢 :sunglasses]'+':blue[ 迎 :sunglasses]'+':green[ ~ :sunglasses]')

    st.write('--------------------------------------------')
    st.text(
    '''这里是Python创赛营根据地，由各位优秀的同学们一起建设。
    你是否为了程序的报错而抓耳挠腮？或者是为找不到小黑子而烦恼呢？
    那这里，你都可以解决这些'''
    )

    st.snow()

    name = st.text_input("请输入你的名字：")
    st.text('↑在此文字上输入')
    st.text('你好呀'+name)
def page1():
    global PCL_file,haigui2_file,classin64_file,todesk_file
    with open(PCL_file,"rb") as file:
        btn = st.download_button(
            label="我的世界PCL启动器下载",
            data=file,
            file_name="PCL我的世界启动器.exe",
            mime="application/octet-stream"
        )
    with open(todesk_file,"rb") as file:
        btn = st.download_button(
            label="ToDesk 安装包下载",
            data=file,
            file_name="ToDesk 安装包.exe",
            mime="application/octet-stream"
        )
    if st.button('classin安装包64位'):
        wget.download(classin64_file, 'classin安装包64位.exe')
    if st.button('海龟编辑器2安装包64位'):
        wget.download(haigui2_file,'海龟编辑器2安装包64位.exe')
    st.text("下载打开后如果出错，请移动到其他文件夹并以管理员权限运行！！！")
    st.image('001.png')
    st.snow()
def page2():
    st.write('纯音乐')
    st.write('Void')
    with open('Void.mp3','rb') as f:
        mymp3_0 = f.read()
    st.audio(mymp3_0,format='audio/mp3',start_time=0)
    st.write('【FREE】lucky')
    with open('FREElucky.mp3','rb') as f:
        mymp3_2 = f.read()
    st.audio(mymp3_2,format='audio/mp3',start_time=0)
    st.write('Daylight')
    with open('Daylight.mp3','rb') as f:
        mymp3_3 = f.read()
    st.audio(mymp3_3,format='audio/mp3',start_time=0)
    st.write('--------------------------------------')
    st.write('英文歌')
    st.write('See You Again')
    with open('SeeYouAgain.mp3','rb') as f:
        mymp3_4 = f.read()
    st.audio(mymp3_4,format='audio/mp3',start_time=0)
    st.write('Love is gone')
    with open('loveisgone.mp3','rb') as f:
        mymp3_5 = f.read()
    st.audio(mymp3_5,format='audio/mp3',start_time=0)
    st.write('Stay')
    with open('stay.mp3','rb') as f:
        mymp3_6 = f.read()
    st.audio(mymp3_6,format='audio/mp3',start_time=0)
    st.write('---------------------------------------------')
    st.write('*下载音乐后如为文件，请直接用Window音频播放器或QQ音乐播放即可！')
def page5():
    st.write(":volcano:图片换色小程序:volcano:")
    uploaded_file = st.file_uploader("上传图片", type=['png', 'jpeg', 'jpg'])
    print(uploaded_file)
    if uploaded_file:
        # 获取图片文件的名称、类型和大小
        file_name = uploaded_file.name
        file_type = uploaded_file.type
        file_size = uploaded_file.size
        img = Image.open(uploaded_file)
        st.image(img)
        st.image(img_change(img,0, 2, 1))
def page6():
    st.write('私人词典')
    # 从本地文件中将词典信息读取出来，并存储在列表中
    with open('words_space.txt', 'r', encoding='utf-8') as f:
        words_list = f.read().split('\n')
    # 将列表中的每一项内容再进行分割，分为“编号、单词、解释”
    for i in range(len(words_list)):
        words_list[i] = words_list[i].split('#')
    # 将列表中的内容导入字典，方便查询，格式为“单词：编号、解释”
    words_dict = {}
    for i in words_list:
        words_dict[i[1]] = [int(i[0]), i[2]]
    # 从本地文件中将单词的查询次数读取出来，并存储在列表中
    with open('check_out_times.txt', 'r', encoding='utf-8') as f:
        times_list = f.read().split('\n')
    # 将列表转为字典
    for i in range(len(times_list)):
        times_list[i] = times_list[i].split('#')
    times_dict = {}
    for i in times_list:
        times_dict[int(i[0])] = int(i[1])#编号：次数
    # 创建输入框
    word = st.text_input('请输入要查询的单词')
    # 显示查询内容
    if word in words_dict:
        st.write(words_dict[word])
        n = words_dict[word][0]#查找编号
        if n in times_dict:
            times_dict[n] += 1
        else:
            times_dict[n] = 1
        with open('check_out_times.txt', 'w', encoding='utf-8') as f:
            message = ''
            for k, v in times_dict.items():#k是编号，v是次数
                message += str(k) +  '#' + str(v) + '\n'
            message = message[:-1]
            f.write(message)
        st.write('查询次数：', times_dict[n])
        if word == 'python':
            st.code('''
                    # 恭喜你触发彩蛋，这是一行python代码
                    print('hello world')''')
def page7():
    '''我的留言区'''
    st.write('我的留言区')
    # 从文件中加载内容，并处理成列表
    with open('leave_messages.txt', 'r', encoding='utf-8') as f:
        messages_list = f.read().split('\n')
    for i in range(len(messages_list)):
        messages_list[i] = messages_list[i].split('#')
    for i in messages_list:
        if i[1] == '阿短':
            with st.chat_message('🌞'):
                st.write(i[1],':',i[2])
        elif i[1] == '编程猫':
            with st.chat_message('🍥'):
                st.write(i[1],':',i[2])#st.text(i[1]+':'+i[2])
    name = st.selectbox('我是……', ['阿短', '编程猫'])
    new_message = st.text_input('想要说的话……')
    if st.button('留言'):
        messages_list.append([str(int(messages_list[-1][0])+1), name, new_message])
        with open('leave_messages.txt', 'w', encoding='utf-8') as f:
            message = ''
            for i in messages_list:
                message += i[0] + '#' + i[1] + '#' + i[2] + '\n'
            message = message[:-1]
            f.write(message)
def page8():
    st.write('----------------------------------------------------------------------')
    st.write('调查问卷')
    with open('reply.txt','a+',encoding='utf-8') as reply:
        reply.truncate(0)
        que1 = st.text_input('1.你对这个网页的评价：')
        reply.write('1.'+que1)
        que2 = st.text_input('2.你还想添加些什么？')
        reply.write('\n2.'+que2)
        que3 = st.text_input('3.我们哪里可以优化：')
        reply.write('\n3.'+que3)
        que4 = st.text_input('4.音乐还可以添加什么：')
        reply.write('\n4.'+que4)
        que5 = st.text_input('5.你喜欢什么游戏：')
        reply.write('\n5.'+que5)
        if st.button("提交"):
            reply.truncate(0)
            st.write('提交成功！')
def page9():
    st.text('网页导航')
    help_page9('百度','https://www.baidu.com')
    help_page9('Edge搜索','https://cn.bing.com/')
    help_page9('百度翻译','https://fanyi.baidu.com')
    help_page9('哔哩哔哩','https://www.bilibili.com')
    help_page9('抖音','https://www.douyin.com')
    help_page9('爱奇艺','https://www.iqiyi.com')
    help_page9('github','https://github.com')
    help_page9('淘宝','https://www.taobao.com')
    help_page9('我的世界中文网','https://www.minecraftzw.com')
    help_page9('编程猫官网','https://www.codemao.cn')
    help_page9('编程猫神奇代码岛','https://box3.codemao.cn')
def page10():
    st.write('时间')
    st.write('*刷新网页才能查看当前时间')
    st.write('======================================================================')
    st.write(time.strftime("%Y-%M-%d %H:%M:%S"))
def page11():
    help_page9('streamlit官网','https://streamlit.io/')
    st.write('本网页使用python-streamlit搭建')
    st.write('streamlit版本:1.30.0')
    st.write('网页版本：4.8.5')
    st.write('感谢大家的支持！')


if page == '首页':
    page_home()
elif page == '下载':
    page1()
elif page == '音乐':
    page2()
elif page == '图片处理':
    page5()
elif page == '我的私人词典':
    page6()
elif page == '留言区':
    page7()
elif page == '调查':
    page8()
elif page == '网页导航':
    page9()
elif page == '时间':
    page10()
elif page == '关于':
    page11()


