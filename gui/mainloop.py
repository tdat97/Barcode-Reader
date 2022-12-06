from gui.configure import configure
from utils import tool, process, db
from utils.camera import SentechCam
from utils.logger import logger
from collections import defaultdict
import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2
from queue import Queue
from threading import Thread
import time
import serial
import os

TITLE = "Machine Vision System"
ICON_PATH = "./gui/eye.ico"
NOT_FOUND_PATH = "./image/not_found"
SERIAL_PORT = "COM1"

class VisualControl():
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(ICON_PATH)
        self.screenheight = self.root.winfo_screenheight()
        self.screenwidth = self.root.winfo_screenwidth()
        self.root.title(TITLE)
        self.root.state("zoomed")
        self.root.geometry(f"{self.screenwidth//3*2}x{self.screenheight//3*2}")
        self.root.minsize(self.screenwidth//3*2, self.screenheight//3*2)
        self.fsize_factor = np.linalg.norm((self.screenheight, self.screenwidth)) / np.linalg.norm((1080,1920))
        
        # 디자인
        configure(self)
        
        # 기타 변수 초기화
        self.current_origin_image = None#np.zeros((100,100,3), dtype=np.uint8)
        self.current_image = None
        self.not_found_path = NOT_FOUND_PATH
        self.sys_msg_list = []
        self.write_sys_msg("안녕하세요.")
        
        # 쓰레드 통신용
        self.stop_signal = True
        self.raw_Q = Queue()
        self.image_Q = Queue()
        self.data_Q = Queue()
        self.db_Q = Queue()
        
        # db 정보 가져오기
        self.connection, self.cursor = db.connect_db()
        self.code2name, self.code2cnt = db.load_db(self) # (dict, defaultdict) # 카운트는 오늘 날짜만 가져와서 카운트
        logger.info("Loaded DB.")
        
        # 초기정보 적용
        self.update_gui(None, init=True)
        self.single_cnt.configure(text='')
        
        # 카메라, 보드 연결
        self.cam = self.get_cam()
        self.serial = self.get_serial(SERIAL_PORT)
        self.show_device_state()
            
    #######################################################################
    def write_sys_msg(self, msg):
        msg = tool.get_time_str(True) + " >>> " + str(msg)
        self.sys_msg_list.append(msg)
        if len(self.sys_msg_list) > 3: self.sys_msg_list.pop(0)
        
        msg_concat = '\n'.join(self.sys_msg_list)
        self.msg_label.configure(text=msg_concat)
    
    #######################################################################
    def start(self):
        logger.info("Start button clicked.")
        
        if (not self.cam) or (not self.serial): return
        
        self.stop_signal = False
        
        tool.clear_serial(self.serial)
        tool.clear_Q(self.raw_Q)
        tool.clear_Q(self.image_Q)
        tool.clear_Q(self.data_Q)
        tool.clear_Q(self.db_Q)
        
        Thread(target=self.stop_signal_eater, args=(), daemon=True).start()
        Thread(target=self.image_eater, args=(), daemon=True).start()
        Thread(target=self.data_eater, args=(), daemon=True).start()
        Thread(target=process.sensor2shot, args=(self,), daemon=True).start()
        Thread(target=process.process, args=(self,), daemon=True).start()
        Thread(target=db.db_process, args=(self,), daemon=True).start()
        
        self.run_button.configure(text="Waiting...", command=lambda:time.sleep(0.1))
        self.sub_button1.configure(text="", command=lambda:time.sleep(0.1))
        self.sub_button2.configure(text="", command=lambda:time.sleep(0.1))
        time.sleep(0.5)
        self.run_button.configure(text="중지", command=self.stop)
        self.sub_button1.configure(text="", command=lambda:time.sleep(0.1))
        self.sub_button2.configure(text="", command=lambda:time.sleep(0.1))
        
        self.write_sys_msg("판독모드 시작! (센서에 제품이 지나갈때 판독)")
        
    #######################################################################
    def stop(self):
        logger.info("Stop button clicked.")
        self.stop_signal = True
    
    def stop_signal_eater(self):
        while True:
            time.sleep(0.01)
            if self.stop_signal:
                self.run_button.configure(text="Waiting...", command=lambda:time.sleep(0.1))
                self.sub_button1.configure(text="", command=lambda:time.sleep(0.1))
                self.sub_button2.configure(text="", command=lambda:time.sleep(0.1))
                time.sleep(0.5)
                self.run_button.configure(text="시작", command=self.start)
                self.sub_button1.configure(text="촬영모드", command=self.shotmode)
                self.sub_button2.configure(text="", command=lambda:time.sleep(0.1))
                
                self.image_label.configure(image=None)
                self.image_label.image = None
                self.ok_label.configure(text='')
                
                self.write_sys_msg("중지됨.")
                break
    
    #######################################################################
    def shotmode(self):
        logger.info("Shotmode button clicked.")
        self.stop_signal = False
        
        tool.clear_Q(self.raw_Q)
        
        Thread(target=self.stop_signal_eater, args=(), daemon=True).start()
        Thread(target=self.image_eater, args=(), daemon=True).start()
        Thread(target=self.raw_Q2image_Q, args=(), daemon=True).start()
        
        self.run_button.configure(text="", command=lambda:time.sleep(0.1))
        self.sub_button1.configure(text="Waiting...", command=lambda:time.sleep(0.1))
        self.sub_button2.configure(text="", command=lambda:time.sleep(0.1))
        time.sleep(1)
        self.run_button.configure(text="중지", command=self.stop)
        self.sub_button1.configure(text="촬영", command=lambda:process.raw_shot(self))
        self.sub_button2.configure(text="저장", command=self.save)
        
        self.write_sys_msg("촬영모드 시작.")
        
    def raw_Q2image_Q(self):
        while True:
            time.sleep(0.01)
            if self.stop_signal: break
            if not self.raw_Q.empty():
                img = self.raw_Q.get()
                self.image_Q.put(img)
    
    def save(self):
        logger.info("Save button clicked.")
        if self.current_origin_image is None: return
        filename = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="이미지 저장",
                                          filetypes=(("IMG files", "*.jpg"), ))
        filename = filename.split(".jpg")[0]
        if filename:
            res = cv2.imwrite(f"{filename}.jpg", self.current_origin_image[:,:,::-1])
            text = "저장됨." if res else "저장실패."
            logger.info(f"{filename}.jpg " + text)
            self.write_sys_msg(text)
    
    #######################################################################
    def __auto_resize_img(self):
        h, w = self.current_origin_image.shape[:2]
        ratio = h/w
        wh = self.image_frame.winfo_height() - 24
        ww = self.image_frame.winfo_width() - 24
        wratio = wh/ww
        
        if ratio < wratio: size, target = ww, 'w'
        else: size, target = wh, 'h'
        self.current_image = tool.fix_ratio_resize_img(self.current_origin_image, size=size, target=target)

    def image_eater(self):
        current_winfo = self.image_frame.winfo_width(), self.image_frame.winfo_height()
        while True:
            time.sleep(0.02)
            if self.stop_signal: break
            last_winfo = self.image_frame.winfo_width(), self.image_frame.winfo_height()
            
            if current_winfo == last_winfo and self.image_Q.empty(): continue
            if current_winfo != last_winfo: current_winfo = last_winfo
            if not self.image_Q.empty(): self.current_origin_image = self.image_Q.get()[:,:,::-1]
            if self.current_origin_image is None: continue
            
            self.__auto_resize_img()
            imgtk = ImageTk.PhotoImage(Image.fromarray(self.current_image))
            self.image_label.configure(image=imgtk)
            self.image_label.image = imgtk
    
    #######################################################################
    def update_gui(self, code, init=False):
        # day_cnt gui
        day_cnt_all = sum(self.code2cnt.values())
        day_cnt_ng = self.code2cnt[None]
        day_cnt_ok = day_cnt_all - day_cnt_ng
        self.day_cnt_all.configure(text=day_cnt_all)
        self.day_cnt_ok.configure(text=day_cnt_ok)
        self.day_cnt_ng.configure(text=day_cnt_ng)
        if init: return
        
        # single_cnt
        if code is None: name = "인식실패"
        elif code in self.code2name: name = self.code2name[code]
        else: name = "새로운 제품"
        self.name_label.configure(text=name)
        self.single_cnt.configure(text=self.code2cnt[code])
        
        # OK, NG
        if code: self.ok_label.configure(text='OK', fg='#6f6')
        else: self.ok_label.configure(text='NG', fg='#f00')
    
    def data_eater(self):
        while True:
            time.sleep(0.02)
            if self.stop_signal: break
            if self.data_Q.empty(): continue
            
            code = self.data_Q.get()
            self.code2cnt[code] += 1
            self.update_gui(code)
    
    #######################################################################
    def go_directory(self, path):
        path = os.path.realpath(path)
        os.startfile(path)
    
    #######################################################################
    def get_cam(self):
        try:
            cam = SentechCam(logger=logger, ExposureTime=2500)
            for _ in range(3): cam.get_image()
            logger.info("Cam Started.")
            return cam
        except Exception as e:
            logger.error(e)
            self.write_sys_msg(e)
            return None
    
    def get_serial(self, port):
        try:
            my_serial = serial.Serial(port, 9600, timeout=0, bytesize=serial.EIGHTBITS, 
                                      stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_ODD)
            
            time.sleep(1.2)
            my_serial.write(b'r')
            time.sleep(0.05)
            if my_serial.read(1) == b'': 
                raise Exception("Serial is unresponsive.")
            logger.info("Serial Opened.")
            return my_serial
        except Exception as e:
            logger.error(e)
            self.write_sys_msg(e)
            return None
    
    def show_device_state(self):
        text = f"Cam state : {bool(self.cam)}   Serial state : {bool(self.serial)}"
        self.write_sys_msg(text)
        if (not self.cam) or (not self.serial):
            self.run_button.configure(text="", command=lambda:time.sleep(0.1))
            self.sub_button1.configure(text="", command=lambda:time.sleep(0.1))
            self.sub_button2.configure(text="", command=lambda:time.sleep(0.1))