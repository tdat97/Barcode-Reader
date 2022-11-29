import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font

BG_COLOR = "#546C86"

def configure(self):
    self.root.configure(bg=BG_COLOR)
    
    # OK + NG + 시스템메시지 프레임
    self.sys_frame = tk.Frame(self.root, relief=None, bd=10, bg=BG_COLOR)#"solid"
    self.sys_frame.place(relx=0.0, rely=0.0, relwidth=0.7, relheight=0.15)
    self.ok_label = tk.Label(self.sys_frame, bg=BG_COLOR, relief=None, bd=10)
    self.ok_label.place(relx=0.0, rely=0.0, relwidth=0.2, relheight=1.0)
    self.ok_label['font'] = font.Font(family='Helvetica', size=90, weight='bold')
    self.ok_label.configure(text='OK', fg='#6f6', anchor='center')
    # self.ok_label.configure(text='NG', fg='#f00', anchor='center')
    self.msg_label = tk.Label(self.sys_frame, anchor="w", bg=BG_COLOR, relief="solid", bd=1)
    self.msg_label.place(relx=0.2, rely=0.0, relwidth=0.8, relheight=1.0)
    self.msg_label['font'] = font.Font(family='Helvetica', size=20, weight="normal")
    self.msg_label.configure(text='SYSTEM MESSAGE', fg='#fff', justify='left', padx=50)
    
    # 이미지 프레임
    self.image_frame = tk.Frame(self.root, relief=None, bd=10, bg=BG_COLOR)#"solid"
    self.image_frame.place(relx=0.0, rely=0.15, relwidth=0.7, relheight=0.85)
    self.image_label = tk.Label(self.image_frame, anchor="center", bg="#8497B0")
    self.image_label.pack(expand=True, fill="both")
    
    # 버튼 프레임 ( 시작, 중단, 촬영 )
    self.button_frame = tk.Frame(self.root, relief=None, bd=10, bg=BG_COLOR)
    self.button_frame.place(relx=0.7, rely=0.0, relwidth=0.3, relheight=0.15)
    self.run_button = tk.Button(self.button_frame, text="", bd=7, bg="#b5b5b5")
    self.run_button.place(relx=0, rely=0, relwidth=0.33, relheight=1.0)
    self.run_button['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.run_button.configure(text="시작", command=self.start)
    self.sub_button1 = tk.Button(self.button_frame, text="", bd=7, bg="#b5b5b5")
    self.sub_button1.place(relx=0.33, rely=0, relwidth=0.33, relheight=1.0)
    self.sub_button1['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.sub_button1.configure(text="촬영모드", command=self.shotmode)
    self.sub_button2 = tk.Button(self.button_frame, text="", bd=7, bg="#b5b5b5")
    self.sub_button2.place(relx=0.66, rely=0, relwidth=0.34, relheight=1.0)
    self.sub_button2['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.sub_button2.configure(text="", command=None)
    
    # 누적수량 프레임
    self.stack_frame = tk.Frame(self.root, relief=None, bd=10, bg=BG_COLOR)
    self.stack_frame.place(relx=0.7, rely=0.15, relwidth=0.3, relheight=0.40)
    self.stack_frame.configure(highlightbackground="#00b0f0", highlightthickness=4)
    self.temp_label = tk.Label(self.stack_frame, text='하루 성공수량')
    self.temp_label.place(relx=0.0, rely=0.0, relwidth=0.49, relheight=0.32)
    self.temp_label['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.temp_label.configure(fg='#00b0f0', bg="#335879")
    self.temp_label = tk.Label(self.stack_frame, text='하루 실패수량')
    self.temp_label.place(relx=0.0, rely=0.34, relwidth=0.49, relheight=0.32)
    self.temp_label['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.temp_label.configure(fg='#00b0f0', bg="#335879")
    self.temp_label = tk.Label(self.stack_frame, text='하루 총 생산량')
    self.temp_label.place(relx=0.0, rely=0.68, relwidth=0.49, relheight=0.32)
    self.temp_label['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.temp_label.configure(fg='#00b0f0', bg="#335879")
    self.day_cnt_ok = tk.Label(self.stack_frame, text='9999', padx=20)
    self.day_cnt_ok.place(relx=0.51, rely=0.0, relwidth=0.49, relheight=0.32)
    self.day_cnt_ok['font'] = font.Font(family='Helvetica', size=40, weight='bold')
    self.day_cnt_ok.configure(fg='#000', bg="#deebf7", anchor='e')
    self.day_cnt_ng = tk.Label(self.stack_frame, text='9999', padx=20)
    self.day_cnt_ng.place(relx=0.51, rely=0.34, relwidth=0.49, relheight=0.32)
    self.day_cnt_ng['font'] = font.Font(family='Helvetica', size=40, weight='bold')
    self.day_cnt_ng.configure(fg='#000', bg="#deebf7", anchor='e')
    self.day_cnt_all = tk.Label(self.stack_frame, text='9999', padx=20)
    self.day_cnt_all.place(relx=0.51, rely=0.68, relwidth=0.49, relheight=0.32)
    self.day_cnt_all['font'] = font.Font(family='Helvetica', size=40, weight='bold')
    self.day_cnt_all.configure(fg='#000', bg="#deebf7", anchor='e')
    
    
    # 품목명 + 현재수량 + 미판독보기 프레임
    self.product_frame = tk.Frame(self.root, relief=None, bd=6, bg=BG_COLOR)
    self.product_frame.place(relx=0.70, rely=0.55, relwidth=0.3, relheight=0.3)
    self.product_frame.configure(highlightbackground="#85bc50", highlightthickness=4)
    self.name_label = tk.Label(self.product_frame, text='품목명')
    self.name_label.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.48)
    self.name_label['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.name_label.configure(fg='#595959', bg="#deebf7")
    
    self.temp_label = tk.Label(self.product_frame, text='수량')
    self.temp_label.place(relx=0.0, rely=0.52, relwidth=0.49, relheight=0.48)
    self.temp_label['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    self.temp_label.configure(fg='#85bc50', bg="#333f50")
    
    self.single_cnt = tk.Label(self.product_frame, text='9999', padx=20)
    self.single_cnt.place(relx=0.51, rely=0.52, relwidth=0.49, relheight=0.48)
    self.single_cnt['font'] = font.Font(family='Helvetica', size=40, weight='bold')
    self.single_cnt.configure(fg='#000', bg="#e1f7ff", anchor='e')

    # 미판독보기 프레임
    self.miss_frame = tk.Frame(self.root, bd=10, bg=BG_COLOR)
    self.miss_frame.place(relx=0.7, rely=0.85, relwidth=0.3, relheight=0.15)
    self.miss_button = tk.Button(self.miss_frame, bd=7, bg="#5b9bd5")
    self.miss_button.place(relx=0, rely=0, relwidth=1, relheight=1)
    self.miss_button['font'] = font.Font(family='Helvetica', size=20, weight='bold')
    func = lambda:self.go_directory(self.not_found_path)
    self.miss_button.configure(fg="#fff", text="판독 실패 보기", command=func)
    
    