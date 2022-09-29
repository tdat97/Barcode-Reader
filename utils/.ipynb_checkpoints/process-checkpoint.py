from utils.logger import logger
from utils.detect_code import get_qrcode, get_barcode, draw_box_text
from utils.tool import get_time_str
import time
import cv2
import os

SAVE_PATH = "./image"

def raw_shot(self):
    self.serial.write(b'o')
    img = self.cam.get_image()
    self.serial.write(b'x')
    self.raw_Q.put(img)
    
def sensor2shot(self):
    try:
        while True:
            time.sleep(0.01)
            if self.stop_signal: break
            
            sensor_value = self.serial.read(1)
            if sensor_value == b'': continue
            raw_shot(self)
            
    except Exception as e:
        logger.error(f"[sensor2shot]{e}")
        self.msg_label.configure(text=e)
        self.stop_signal = True

def process(self):
    try:
        while True:
            time.sleep(0.01)
            if self.stop_signal: break
            
            # get image
            if self.raw_Q.empty(): continue
            img = self.raw_Q.get()
            
            # save raw img
            time_str = get_time_str()
            path = os.path.join(SAVE_PATH, "raw", f"{time_str}.jpg")
            cv2.imwrite(path, img)
            
            # get code
            data, poly_boxes = get_qrcode(img)
            if not data: 
                logger.info("QRcode is not found.")
                data, poly_boxes, debug_img = get_barcode(img)
                # save debug img
                if debug_img is not None:
                    path = os.path.join(SAVE_PATH, "debug", f"{time_str}.jpg")
                    cv2.imwrite(path, debug_img)
                
            if not data:
                logger.info("Barcode is not found.")
                data = None
                
            if data:
                for v in data: logger.info(f"code : {v}")
                img = draw_box_text(img, data, poly_boxes)
                data = data[0]
                # save anno img
                path = os.path.join(SAVE_PATH, "anno", f"{time_str}.jpg")
                cv2.imwrite(path, img)
            
            self.image_Q.put(img)
            self.data_Q.put(data)
        
    except Exception as e:
        logger.error(f"[process]{e}")
        self.msg_label.configure(text=e)
        self.stop_signal = True