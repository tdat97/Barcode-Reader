import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font

def configure(self):
    # 프레임1
    self.image_frame = tk.Frame(self.root, relief="solid", bd=1)#"solid"
    self.image_frame.place(relx=0.0, rely=0.0, relwidth=0.7, relheight=1)
    # 프레임1 - 라벨
    self.image_label = tk.Label(self.image_frame, anchor="center")
    # self.image_label.place(relx=0.0, rely=0.0)
    self.image_label.pack(expand=True, fill="both")
    
    # 프레임2
    self.state_frame = tk.Frame(self.root, relief=None, bd=10)
    self.state_frame.place(relx=0.7, rely=0.0, relwidth=0.3, relheight=1)
    # 프레임2 - 버튼
    self.run_button = tk.Button(self.state_frame, text="", command=None, bd=3)
    self.run_button.place(relx=0, rely=0, relwidth=0.33, relheight=0.105)
    self.run_button['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.run_button.configure(text="START", command=self.start)
    # 프레임2 - 버튼1
    self.sub_button1 = tk.Button(self.state_frame, text="", command=None, bd=3)
    self.sub_button1.place(relx=0.33, rely=0, relwidth=0.33, relheight=0.105)
    self.sub_button1['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.sub_button1.configure(text="SHOT\nMODE", command=self.shotmode)
    # 프레임2 - 버튼2
    self.sub_button2 = tk.Button(self.state_frame, text="", command=None, bd=3)
    self.sub_button2.place(relx=0.66, rely=0, relwidth=0.34, relheight=0.105)
    self.sub_button2['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.sub_button2.configure(text="", command=None)
    
    # 프레임2 - 프레임
    self.result_frame = tk.Frame(self.state_frame)#, relief="solid", bd=10)
    self.result_frame.place(relx=0.0, rely=0.11, relwidth=1, relheight=0.145)
    self.result_frame.configure(highlightthickness=4, highlightbackground='#08f')
    # 프레임2 - 프레임 - 라벨1
    self.static_label1 = tk.Label(self.result_frame, text='탐지 결과')
    self.static_label1.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.2)
    self.static_label1['font'] = font.Font(family='Helvetica', size=15, weight='bold')
    self.static_label1.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임 - 라벨2
    self.ok_label = tk.Label(self.result_frame)
    self.ok_label.place(relx=0.0, rely=0.2, relwidth=1, relheight=0.8)
    self.ok_label['font'] = font.Font(family='Helvetica', size=35, weight='bold')
    self.ok_label.configure(text='NONE', fg='#ff0', bg='#333', anchor='center')
    # self.ok_label.configure(text='OK', fg='#ff0', bg='#0cf', anchor='center')
    # self.ok_label.configure(text='FAIL', fg='#ff0', bg='#f30', anchor='center')
    
    # 프레임2 - 프레임2
    self.total_frame = tk.Frame(self.state_frame)#, relief="solid", bd=10)
    self.total_frame.place(relx=0.0, rely=0.26, relwidth=1, relheight=0.155)
    self.total_frame.configure(highlightthickness=4, highlightbackground='#08f')
    # 프레임2 - 프레임2 - 라벨1
    self.static_label2 = tk.Label(self.total_frame, text='전체 통계')
    self.static_label2.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.2)
    self.static_label2['font'] = font.Font(family='Helvetica', size=15, weight='bold')
    self.static_label2.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임2 - 프레임
    self.total_ff = tk.Frame(self.total_frame, bd=10)
    self.total_ff.place(relx=0.0, rely=0.2, relwidth=1, relheight=0.8)
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl = tk.Label(self.total_ff, text='누적 총수량')
    self.total_ffl.place(relx=0.0, rely=0.0, relwidth=0.15, relheight=0.25)
    self.total_ffl['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl1 = tk.Label(self.total_ff, text=f'{10000:d}', relief="solid", bd=1)
    self.total_ffl1.place(relx=0.16, rely=0.0, relwidth=0.15, relheight=0.25)
    self.total_ffl1['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl1.configure(fg='#000', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl = tk.Label(self.total_ff, text='누적 정상')
    self.total_ffl.place(relx=0.32, rely=0.0, relwidth=0.15, relheight=0.25)
    self.total_ffl['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl2 = tk.Label(self.total_ff, text=f'{9900:d}', relief="solid", bd=1)
    self.total_ffl2.place(relx=0.48, rely=0.0, relwidth=0.15, relheight=0.25)
    self.total_ffl2['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl2.configure(fg='#000', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl = tk.Label(self.total_ff, text='누적 미판독')
    self.total_ffl.place(relx=0.64, rely=0.0, relwidth=0.15, relheight=0.25)
    self.total_ffl['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl3 = tk.Label(self.total_ff, text=f'{100:d}', relief="solid", bd=1)
    self.total_ffl3.place(relx=0.80, rely=0.0, relwidth=0.15, relheight=0.25)
    self.total_ffl3['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl3.configure(fg='#000', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl = tk.Label(self.total_ff, text='총 수량')
    self.total_ffl.place(relx=0.0, rely=0.3, relwidth=0.15, relheight=0.25)
    self.total_ffl['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl4 = tk.Label(self.total_ff, text=f'{10000:d}', relief="solid", bd=1)
    self.total_ffl4.place(relx=0.16, rely=0.3, relwidth=0.15, relheight=0.25)
    self.total_ffl4['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl4.configure(fg='#000', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl = tk.Label(self.total_ff, text='정상')
    self.total_ffl.place(relx=0.32, rely=0.3, relwidth=0.15, relheight=0.25)
    self.total_ffl['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl5 = tk.Label(self.total_ff, text=f'{9900:d}', relief="solid", bd=1)
    self.total_ffl5.place(relx=0.48, rely=0.3, relwidth=0.15, relheight=0.25)
    self.total_ffl5['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl5.configure(fg='#000', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl = tk.Label(self.total_ff, text='미판독')
    self.total_ffl.place(relx=0.64, rely=0.3, relwidth=0.15, relheight=0.25)
    self.total_ffl['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 라벨
    self.total_ffl6 = tk.Label(self.total_ff, text=f'{100:d}', relief="solid", bd=1)
    self.total_ffl6.place(relx=0.80, rely=0.3, relwidth=0.15, relheight=0.25)
    self.total_ffl6['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.total_ffl6.configure(fg='#000', anchor='w')
    # 프레임2 - 프레임2 - 프레임 - 버튼
    func = lambda:self.go_directory(self.not_found_path)
    self.init_button = tk.Button(self.total_ff, text="미판독 보기", command=func, bd=2)
    self.init_button.place(relx=0, rely=0.65, relwidth=1, relheight=0.35)
    self.init_button['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    # 프레임2 - 프레임2 - 프레임 - 버튼
    # func = lambda:self.go_directory(self.not_found_path)
    # self.file_button = tk.Button(self.total_ff, text="미판독 보기", command=func, bd=2)
    # self.file_button.place(relx=0.5, rely=0.0, relwidth=0.48, relheight=0.25)
    # self.file_button['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    # 프레임2 - 프레임2 - 프레임 - 버튼
    # self.init_button = tk.Button(self.total_ff, text="초기화", command=self.clear_data, bd=2)
    # self.init_button.place(relx=0, rely=0.65, relwidth=1, relheight=0.35)
    # self.init_button['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    
    # 프레임2 - 프레임3
    self.detail_frame = tk.Frame(self.state_frame)#, relief="solid", bd=10)
    self.detail_frame.place(relx=0.0, rely=0.42, relwidth=1, relheight=0.335)
    self.detail_frame.configure(highlightthickness=4, highlightbackground='#08f')
    # 프레임2 - 프레임3 - 라벨1
    self.static_label3 = tk.Label(self.detail_frame, text='세부 통계')
    self.static_label3.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.10)
    self.static_label3['font'] = font.Font(family='Helvetica', size=15, weight='bold')
    self.static_label3.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임3 - 프레임
    self.detail_ff = tk.Frame(self.detail_frame, relief="solid", bd=0) #####
    self.detail_ff.place(relx=0.0, rely=0.1, relwidth=1, relheight=0.9)
    # 프레임2 - 프레임3 - 프레임 - 라벨(name, ok, ng)
    self.detail_fffl1 = tk.Label(self.detail_ff, text="제품 이름")
    self.detail_fffl1.place(relx=0.0, rely=0.0, relwidth=0.33, relheight=0.1)
    self.detail_fffl2 = tk.Label(self.detail_ff, text="누적 총 수량")
    self.detail_fffl2.place(relx=0.33, rely=0.0, relwidth=0.33, relheight=0.1)
    self.detail_fffl3 = tk.Label(self.detail_ff, text="총 수량")
    self.detail_fffl3.place(relx=0.66, rely=0.0, relwidth=0.31, relheight=0.1)
    # 프레임2 - 프레임3 - 프레임 - 프레임
    self.detail_fff = tk.Frame(self.detail_ff, relief="solid", bd=1) #####
    self.detail_fff.place(relx=0.0, rely=0.1, relwidth=1, relheight=0.9)
    # 프레임2 - 프레임3 - 프레임 - 프레임 - 스크롤
    style = ttk.Style(self.detail_fff)
    style.layout('arrowless.Vertical.TScrollbar', 
         [('Vertical.Scrollbar.trough',
           {'children': [('Vertical.Scrollbar.thumb', 
                          {'expand': '1', 'sticky': 'nswe'})],
            'sticky': 'ns'})])
    self.scrollbar = ttk.Scrollbar(self.detail_fff, style='arrowless.Vertical.TScrollbar')
    self.scrollbar.pack(side="right", fill="y")
    # 프레임2 - 프레임3 - 프레임 - 프레임 - 리스트박스
    func = lambda x,y:(self.scrollbar.set(x,y), self.listbox2.yview("moveto",x), self.listbox3.yview("moveto",x), )
    self.listbox1 = tk.Listbox(self.detail_fff, yscrollcommand=func)
    self.listbox1.place(relx=0.0, rely=0.0, relwidth=0.33, relheight=1)
    func = lambda x,y:self.listbox1.yview("moveto",x)
    self.listbox2 = tk.Listbox(self.detail_fff, yscrollcommand=func)
    self.listbox2.place(relx=0.33, rely=0.0, relwidth=0.33, relheight=1)
    func = lambda x,y:self.listbox1.yview("moveto",x)
    self.listbox3 = tk.Listbox(self.detail_fff, yscrollcommand=func)
    self.listbox3.place(relx=0.66, rely=0.0, relwidth=0.31, relheight=1)
    
    func = lambda x,y:(self.listbox1.yview(x,y), self.listbox2.yview(x,y), self.listbox3.yview(x,y), )
    self.scrollbar.config(command=func)
    
    # 프레임2 - 프레임4
    self.objinfo_frame = tk.Frame(self.state_frame)#, relief="solid", bd=10)
    self.objinfo_frame.place(relx=0.0, rely=0.76, relwidth=1, relheight=0.155)
    self.objinfo_frame.configure(highlightthickness=4, highlightbackground='#08f')
    # 프레임2 - 프레임4 - 라벨1
    self.static_label4 = tk.Label(self.objinfo_frame, text='현재 제품 정보')
    self.static_label4.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.2)
    self.static_label4['font'] = font.Font(family='Helvetica', size=15, weight='bold')
    self.static_label4.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임4 - 프레임
    self.objinfo_ff = tk.Frame(self.objinfo_frame)
    self.objinfo_ff.place(relx=0.0, rely=0.2, relwidth=1, relheight=0.8)
    self.objinfo_ff.columnconfigure(0, weight=1)
    self.objinfo_ff.columnconfigure(1, weight=3)
    # 프레임2 - 프레임4 - 프레임 - 그리드
    self.objinfo_ffl00 = tk.Label(self.objinfo_ff, text="제품 이름")
    self.objinfo_ffl00.grid(row=0, column=0, sticky='w')
    self.objinfo_ffl01 = tk.Label(self.objinfo_ff, text="None")
    self.objinfo_ffl01.grid(row=0, column=1, sticky='w')
    self.objinfo_ffl10 = tk.Label(self.objinfo_ff, text="코드 정보")
    self.objinfo_ffl10.grid(row=1, column=0, sticky='w')
    self.objinfo_ffl11 = tk.Label(self.objinfo_ff, text="None")
    self.objinfo_ffl11.grid(row=1, column=1, sticky='w')
    
    # 프레임2 - 프레임5
    self.system_frame = tk.Frame(self.state_frame)
    self.system_frame.place(relx=0.0, rely=0.92, relwidth=1, relheight=0.08)
    self.system_frame.configure(highlightthickness=4, highlightbackground='#08f')
    # 프레임2 - 프레임5 - 라벨
    self.static_label5 = tk.Label(self.system_frame, text='시스템 메시지')
    self.static_label5.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.4)
    self.static_label5['font'] = font.Font(family='Helvetica', size=15, weight='bold')
    self.static_label5.configure(fg='#fff', bg='#08f', anchor='w')
    # 프레임2 - 프레임5 - 라벨
    self.msg_label = tk.Label(self.system_frame, text='')
    self.msg_label.place(relx=0.0, rely=0.4, relwidth=1, relheight=0.6)
    self.msg_label['font'] = font.Font(family='Helvetica', size=10, weight='bold')
    self.msg_label.configure(fg='#000', bg='#fff', anchor='center')