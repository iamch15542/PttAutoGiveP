# !/usr/bin/python3
#coding=utf-8
#version 3.1.1
import requests
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
from PTTLibrary import PTT


class AutoGive():
    def __init__(self, url):
        self.url = url
        self.choicedata = []
        self.un_sort_list = []
        self.ptt_board = []
        self.ptt_title = []
        self.sort_list = []
        self.tmp_sort_list = []

    # 搜尋網站
    def search(self, web):
        r = requests.get(web)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')

            stories = soup.find_all('span', class_='f3 hl push-userid')
            for s in stories:
                self.un_sort_list.append(s.text)

            #紀錄 標題
            title = soup.find("meta", property="og:title")
            self.ptt_title.append(title["content"])
            text_update('--------------------\n')
            text_update(self.ptt_title[0] + '\n')
            text_update('--------------------\n')

            #紀錄 板名
            board = soup.find_all('span', class_='article-meta-value')
            for s in board:
                self.ptt_board.append(s.text)
            #self.ptt_board[0] 是 Author
            #self.ptt_board[1] 是 board

            #紀錄推噓箭頭
            choice = soup.find_all('span', class_='push-tag')
            k = 0
            for s in choice:
                self.choicedata.append(s.text)
                k += 1

    # 判斷是要發給哪一種tag 再將名單輸入到 tmp_sort_list
    # 模式: 0 = 全都發, 1 = 只發推, 2 = 只發噓, 3 = 只發箭頭, 4 = 發推噓, 5 = 發推箭頭, 6 = 發噓箭頭
    def pushtag(self, select):
        push = ['推', '噓', '→']
        k = 0
        for i in self.choicedata:
            for x in self.choicedata[k]:
                if x in push[0]:
                    if select == '1' or select == '4' or select == '5' or select == '0':
                        self.tmp_sort_list.append(self.un_sort_list[k])
                elif x in push[1]:
                    if select == '2' or select == '4' or select == '6' or select == '0':
                        self.tmp_sort_list.append(self.un_sort_list[k])

                elif x in push[2]:
                    if select == '3' or select == '5' or select == '6' or select == '0':
                        self.tmp_sort_list.append(self.un_sort_list[k])
            k += 1

    # 用來選擇是否要重複ID
    # 0 = 重複ID 1 = 不重複ID
    def check(self, chose, user, cnt):
        for s in self.tmp_sort_list:
            if s == user:
                self.tmp_sort_list.remove(user)
        if chose:
            self.sort_list = list(set(self.tmp_sort_list))
            self.sort_list.sort(key=self.tmp_sort_list.index)
        else:
            self.sort_list = self.tmp_sort_list
        i = 0
        for s in range(cnt):
            text_id_update(self.sort_list[i] + '\n')
            i += 1

    '''
    Give P幣
    '''

    def give(self, user, pwd, cnt, money):
        ptt = PTT.Library(kickOtherLogin=False, _LogLevel=PTT.LogLevel.SLIENT)
        ptt.login(user, pwd)
        text_update('登錄帳號成功\n')
        ptt_cnt = cnt
        i = 0
        while cnt > 0:
            if self.sort_list[i] != user:
                ErrCode = ptt.giveMoney(self.sort_list[i], money, pwd)
                if ErrCode == PTT.ErrorCode.Success:
                    text_update('送P幣給 ' + self.sort_list[i] + ' 成功\n')
                    text_update('--------------------\n')
                else:
                    text_update('送P幣給 ' + self.sort_list[i] + ' 失敗\n')
                    text_update('--------------------\n')
            i += 1
            cnt -= 1

    '''
    修改文章
    '''

    def post(self, user, pwd, cnt, money, post_num):
        ptt = PTT.Library(kickOtherLogin=False, _LogLevel=PTT.LogLevel.SLIENT)
        ptt.login(user, pwd)
        ErrCode, Post = ptt.getPost(self.ptt_board[1], PostIndex=post_num)
        content_data = []
        ptt_content = Post.getContent()
        for data in ptt_content.split('\n'):
            content_data.append(data)
        new_content = ''
        text_update('開始編輯文章內容\n')
        text_update('--------------------\n')
        #送出200個ctrl + y
        ctrly = '\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19'
        cnt_id = 0
        check_point = 0
        end_sentence = '\x15[1;31m' + '以上紅底標記 %d' % int(cnt) + '位，每人 %d' % int(
            money) + '(稅後)發送完成! By PttAutoGive 3.1.1\x15[m' + '\r'
        for i in content_data:
            if '文章網址' in i:
                check_point = 1
            if check_point == 1:
                if '→' in i:
                    pushtype = i[0]
                    push = []
                    for c in i[2:].split(':', 1):
                        push.append(c)
                    pushid = push[0]
                    pushtext = push[1]
                    pushtext_t = pushtext[:-11]
                    pushtime = pushtext[-11:]
                    if cnt != cnt_id and pushid == self.sort_list[cnt_id]:
                        i = '\x15[1;31m' + pushtype + ' \x15[33;41m' + pushid + '\x15[m\x15[33m:' + pushtext_t[:
                                                                                                               -1] + '\x15[m' + pushtime
                        cnt_id += 1
                    else:
                        i = '\x15[1;31m' + pushtype + ' \x15[33m' + pushid + '\x15[m\x15[33m:' + pushtext_t[:
                                                                                                            -1] + '\x15[m' + pushtime
                elif '噓' in i:
                    pushtype = i[0]
                    push = []
                    for c in i[2:].split(':', 1):
                        push.append(c)
                    pushid = push[0]
                    pushtext = push[1]
                    pushtext_t = pushtext[:-11]
                    pushtime = pushtext[-11:]
                    if cnt != cnt_id and pushid == self.sort_list[cnt_id]:
                        i = '\x15[1;31m' + pushtype + ' \x15[33;41m' + pushid + '\x15[m\x15[33m:' + pushtext_t[:
                                                                                                               -1] + '\x15[m' + pushtime
                        cnt_id += 1
                    else:
                        i = '\x15[1;31m' + pushtype + ' \x15[33m' + pushid + '\x15[m\x15[33m:' + pushtext_t[:
                                                                                                            -1] + '\x15[m' + pushtime
                elif '推' in i:
                    pushtype = i[0]
                    push = []
                    for c in i[2:].split(':', 1):
                        push.append(c)
                    pushid = push[0]
                    pushtext = push[1]
                    pushtext_t = pushtext[:-11]
                    pushtime = pushtext[-11:]
                    if cnt != cnt_id and pushid == self.sort_list[cnt_id]:
                        i = '\x15[1;37m' + pushtype + ' \x15[33;41m' + pushid + '\x15[m\x15[33m:' + pushtext_t[:
                                                                                                               -1] + '\x15[m' + pushtime
                        cnt_id += 1
                    else:
                        i = '\x15[1;37m' + pushtype + ' \x15[33m' + pushid + '\x15[m\x15[33m:' + pushtext_t[:
                                                                                                            -1] + '\x15[m' + pushtime
            elif '作者' in i:
                tmplate = []
                for c in i.split(')'):
                    tmplate.append(c)
                postauthor = tmplate[0][1:]
                cb = postauthor.replace(' ', ':', 1)
                postboard = tmplate[1].lstrip()
                pb = postboard.replace(' ', ':', 1)
                tmp = cb + ') ' + pb
                i = tmp
            elif '標題' in i:
                post_title = i[1:]
                tmp = post_title.replace(' ', ':', 1)
                i = tmp
            elif '時間' in i:
                post_time = i[1:]
                tmp = post_time.replace(' ', ':', 1)
                i = tmp
            elif '────' in i:
                i = ''
            new_content += i
            new_content += '\r'
        new_content += end_sentence
        ErrCode = ptt.editPost(
            self.ptt_board[1], ctrly + new_content, Index=post_num)
        if ErrCode == PTT.ErrorCode.Success:
            ptt.Log('在 %s 修改文章成功!' % self.ptt_board[1])
        else:
            ptt.Log('在 %s 修改文章失敗' % self.ptt_board[1] + str(ErrCode))
        text_update('編輯文章完成！！\n')
        text_update('--------------------\n')
        ptt.logout()
        text_update('登出ptt完畢！！\n')
        text_update('--------------------\n')


# 主程式
if __name__ == "__main__":

    windows = tk.Tk()

    # 標題
    windows.title('PTT自動發錢程式')

    # 視窗大小
    windows.geometry('800x500')

    # 輸入帳號介面
    tk.Label(windows, text='帳號: ').place(x=10, y=20)
    tk.Label(windows, text='密碼: ').place(x=10, y=60)
    tk.Label(windows, text='網址: ').place(x=10, y=100)
    get_user_name = tk.StringVar()
    get_user_pwd = tk.StringVar()
    get_web_url = tk.StringVar()
    user_name = tk.Entry(windows, textvariable=get_user_name).place(x=60, y=20)
    user_pwd = tk.Entry(
        windows, textvariable=get_user_pwd, show='*').place(
            x=60, y=60)
    web_url = tk.Entry(
        windows, textvariable=get_web_url, width=50).place(
            x=60, y=100)

    # 文章編號
    tk.Label(windows, text='文章編號: ').place(x=270, y=20)
    get_post_num = tk.StringVar()
    post_num = tk.Entry(windows, textvariable=get_post_num).place(x=350, y=20)

    # 選擇發錢模式
    tk.Label(windows, text='發錢模式: ').place(x=10, y=140)
    chose_var = tk.StringVar()
    chose_zero = tk.Radiobutton(
        windows, text='全發', variable=chose_var, value='0').place(
            x=80, y=140)
    chose_first = tk.Radiobutton(
        windows, text='發推', variable=chose_var, value='1').place(
            x=140, y=140)
    chose_second = tk.Radiobutton(
        windows, text='發噓', variable=chose_var, value='2').place(
            x=200, y=140)
    chose_third = tk.Radiobutton(
        windows, text='發箭頭', variable=chose_var, value='3').place(
            x=260, y=140)
    chose_four = tk.Radiobutton(
        windows, text='發推噓', variable=chose_var, value='4').place(
            x=330, y=140)
    chose_five = tk.Radiobutton(
        windows, text='發推箭頭', variable=chose_var, value='5').place(
            x=400, y=140)
    chose_six = tk.Radiobutton(
        windows, text='發噓箭頭', variable=chose_var, value='6').place(
            x=480, y=140)

    # 輸入發錢人數
    tk.Label(windows, text='人數: ').place(x=10, y=180)
    people_var = tk.IntVar()
    get_people = tk.Entry(windows, textvariable=people_var).place(x=60, y=180)

    # 是否要重複ID
    tk.Label(windows, text='ID重複: ').place(x=10, y=220)
    repeat_id_var = tk.IntVar()
    repeat_id = tk.Radiobutton(
        windows, text='是', variable=repeat_id_var, value='0').place(
            x=70, y=220)
    repeat_id_one = tk.Radiobutton(
        windows, text='否', variable=repeat_id_var, value='1').place(
            x=110, y=220)

    # 彈出錯誤視窗
    def error_message():
        MessageBox.showerror(title='Warning', message='輸入無效網址，請重新輸入。')

    # 彈出下載完成
    def finish_download():
        messagebox.showerror(title='Finish!!!!', message='下載完成！！！！！！！')

    # 金額
    tk.Label(windows, text='金額: ').place(x=10, y=260)
    money_var = tk.StringVar()
    get_money = tk.Entry(windows, textvariable=money_var).place(x=60, y=260)

    # 輸出文字介面
    textbox = tk.Text(windows, height=10, width=80)
    textbox.place(x=10, y=340)

    # 輸出ID
    tk.Label(windows, text='ID列表: ').place(x=600, y=20)
    textbox_two = tk.Text(windows, height=30, width=25)
    textbox_two.place(x=600, y=40)

    # 結束按鈕
    end_button = tk.Button(
        windows, text='結束程式', width=20, height=1,
        command=windows.destroy).place(
            x=300, y=300)

    # 主程式
    def run():
        url = get_web_url.get()
        user = get_user_name.get()
        pwd = get_user_pwd.get()
        chose = chose_var.get()
        repeat = repeat_id_var.get()
        cnt = people_var.get()
        money = money_var.get()
        postnum = get_post_num.get()
        autogive = AutoGive(url)
        autogive.search(url)
        autogive.pushtag(chose)
        autogive.check(repeat, user, cnt)
        autogive.give(user, pwd, cnt, money)
        autogive.post(user, pwd, cnt, money, postnum)
        finish_download()

    # 顯示目前狀態
    def text_update(word):
        textbox.insert('insert', word)
        textbox.update()

    # 顯示ID名稱
    def text_id_update(pttid):
        textbox_two.insert('insert', pttid)
        textbox_two.update()

    # 啟動
    start_button = tk.Button(
        windows, text='啟動', width=20, height=1, command=run).place(
            x=10, y=300)

    # 主循環
    windows.mainloop()
