from gui.configure import configure
from utils.tool import fix_ratio_resize_img, clear_Q, clear_serial
from utils.camera import SentechCam
from utils.logger import logger
from utils.process import process, raw_shot, sensor2shot
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
        self.current_origin_image = None#np.zeros((100,100,3), dtype=np.uint8)
        self.current_image = None
        configure(self)
        
        self.stop_signal = True
        self.raw_Q = Queue()
        self.image_Q = Queue()
        self.data_Q = Queue()
        self.data_dict = defaultdict(int)
        self.data_unique_list = []
        
        self.cam = self.get_cam()
        self.serial = self.get_serial("COM5")
        self.show_device_state()
        
    def get_cam(self):
        try:
            cam = SentechCam(logger=logger)
            for _ in range(3): cam.get_image()
            logger.info("Cam Started.")
            return cam
        except Exception as e:
            logger.error(e)
            self.msg_label.configure(text=e)
            return None
    
    def get_serial(self, port):
        try:
            my_serial = serial.Serial(port, 9600, timeout=0, bytesize=serial.EIGHTBITS, 
                                      stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_ODD)
            logger.info("Serial Opened.")
            return my_serial
        except Exception as e:
            logger.error(e)
            self.msg_label.configure(text=e)
            return None
    
    def show_device_state(self):
        text = f"Cam state : {bool(self.cam)}     Serial state : {bool(self.serial)}"
        self.msg_label.configure(text=text)
        if (not self.cam) or (not self.serial):
            self.run_button.configure(text="", command=None)
            self.sub_button1.configure(text="", command=None)
            self.sub_button2.configure(text="", command=None)
    
    def start(self):
        logger.info("Start button clicked.")
        
        if (not self.cam) or (not self.serial): return
        
        self.stop_signal = False
        self.total_ffl1.configure(text=sum(self.data_dict.values()))
        
        clear_serial(self.serial)
        clear_Q(self.raw_Q)
        clear_Q(self.image_Q)
        clear_Q(self.data_Q)
        
        Thread(target=self.stop_signal_eater, args=(), daemon=True).start()
        Thread(target=self.image_eater, args=(), daemon=True).start()
        Thread(target=self.data_eater, args=(), daemon=True).start()
        Thread(target=sensor2shot, args=(self,), daemon=True).start()
        Thread(target=process, args=(self,), daemon=True).start()
        
        self.run_button.configure(text="Waiting...", command=lambda:time.sleep(1))
        self.sub_button1.configure(text="", command=None)
        self.sub_button2.configure(text="", command=None)
        time.sleep(1)
        self.run_button.configure(text="STOP", command=self.stop)
        self.sub_button1.configure(text="", command=None)
        self.sub_button2.configure(text="", command=None)
        
        
    #######################################################################
    def stop(self):
        logger.info("Stop button clicked.")
        self.stop_signal = True
    
    def stop_signal_eater(self):
        while True:
            time.sleep(0.01)
            if self.stop_signal:
                self.run_button.configure(text="Waiting...", command=lambda:time.sleep(1))
                self.sub_button1.configure(text="", command=None)
                self.sub_button2.configure(text="", command=None)
                time.sleep(1)
                self.run_button.configure(text="START", command=self.start)
                self.sub_button1.configure(text="SHOT\nMODE", command=self.shotmode)
                self.sub_button2.configure(text="", command=None)
                
                self.image_label.configure(image=None)
                self.image_label.image = None
                self.ok_label.configure(text='NONE', fg='#ff0', bg='#333', anchor='center')
                break
    
    #######################################################################
    def shotmode(self):
        logger.info("Shotmode button clicked.")
        self.stop_signal = False
        
        clear_Q(self.raw_Q)
        
        Thread(target=self.stop_signal_eater, args=(), daemon=True).start()
        Thread(target=self.image_eater, args=(), daemon=True).start()
        Thread(target=self.raw_Q2image_Q, args=(), daemon=True).start()
        
        self.run_button.configure(text="", command=None)
        self.sub_button1.configure(text="Waiting...", command=lambda:time.sleep(1))
        self.sub_button2.configure(text="", command=None)
        time.sleep(1)
        self.run_button.configure(text="STOP", command=self.stop)
        self.sub_button1.configure(text="SHOT", command=lambda:raw_shot(self))
        self.sub_button2.configure(text="SAVE", command=self.save)
        
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
        filename = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save file",
                                          filetypes=(("IMG files", "*.jpg"), ))
        filename = filename.split(".jpg")[0]
        if filename:
            res = cv2.imwrite(f"{filename}.jpg", self.current_origin_image[:,:,::-1])
            text = "Saved." if res else "Not Saved."
            logger.info(f"{filename}.jpg " + text)
            self.msg_label.configure(text=text)
    
    
    #######################################################################
    def __auto_resize_img(self):
        h, w = self.current_origin_image.shape[:2]
        ratio = h/w
        wh = self.image_frame.winfo_height() - 24
        ww = self.image_frame.winfo_width() - 24
        wratio = wh/ww
        
        if ratio < wratio: size, target = ww, 'w'
        else: size, target = wh, 'h'
        self.current_image = fix_ratio_resize_img(self.current_origin_image, size=size, target=target)
                                                 
    
    def image_eater(self):
        current_winfo = self.image_frame.winfo_width(), self.image_frame.winfo_height()
        while True:
            time.sleep(0.02)
            if self.stop_signal: break
            last_winfo = self.image_frame.winfo_width(), self.image_frame.winfo_height()
            
            if current_winfo == last_winfo and self.image_Q.empty(): continue
            if current_winfo != last_winfo: current_winfo = last_winfo
            if not self.image_Q.empty(): self.current_origin_image = self.image_Q.get()[:,:,::-1]
            
            self.__auto_resize_img()
            imgtk = ImageTk.PhotoImage(Image.fromarray(self.current_image))
            self.image_label.configure(image=imgtk)
            self.image_label.image = imgtk
    
    #######################################################################
    def update_data(self, code_data):
        self.data_dict[code_data] += 1
        if not code_data in self.data_unique_list:
            self.listbox1.insert(len(self.data_unique_list), code_data)
            self.data_unique_list.append(code_data)
        idx = self.data_unique_list.index(code_data)
        self.listbox4.delete(idx)
        self.listbox4.insert(idx, self.data_dict[code_data])
        self.total_ffl1.configure(text=sum(self.data_dict.values()))
        
    def clear_data(self):
        self.data_dict = defaultdict(int)
        for i in range(len(self.data_unique_list)):
            self.listbox1.delete(i)
            self.listbox4.delete(i)
        self.total_ffl1.configure(text=0)
    
    def data_eater(self):
        while True:
            time.sleep(0.02)
            if self.stop_signal: break
            if self.data_Q.empty(): continue
            
            code_data = self.data_Q.get()
            if code_data:
                self.ok_label.configure(text='OK', fg='#ff0', bg='#0cf', anchor='center')
                self.objinfo_ffl11.configure(text=code_data)
                self.update_data(code_data)
            else:
                self.ok_label.configure(text='FAIL', fg='#ff0', bg='#f30', anchor='center')
                self.objinfo_ffl11.configure(text="None")
    
    #######################################################################
        
            