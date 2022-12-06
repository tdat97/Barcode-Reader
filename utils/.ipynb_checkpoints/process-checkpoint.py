from utils.logger import logger
from utils.detect_code import get_qrcode, get_barcode, draw_box_text
from utils.tool import get_time_str
import time
import cv2
import os

SAVE_PATH = "./image"
path = os.path.join(SAVE_PATH, "anno")
if not os.path.isdir(path): os.mkdir(path)
path = os.path.join(SAVE_PATH, "debug")
if not os.path.isdir(path): os.mkdir(path)
path = os.path.join(SAVE_PATH, "raw")
if not os.path.isdir(path): os.mkdir(path)
path = os.path.join(SAVE_PATH, "not_found")
if not os.path.isdir(path): os.mkdir(path)


def raw_shot(self):
    self.serial.write(b'o')
    time.sleep(0.015)
    img = self.cam.get_image()
    self.serial.write(b'x')
    if img is None:
        logger.error("Raw Image is None !!")
        return
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
        self.write_sys_msg(e)
        self.stop_signal = True

def process(self):
    try:
        while True:
            time.sleep(0.01)
            if self.stop_signal: break
            start_time = time.time()
            
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
                path = os.path.join(SAVE_PATH, "not_found", f"{time_str}.jpg")
                cv2.imwrite(path, img)
                
            if data:
                for v in data:
                    logger.info(f"code : {v}")
                    #self.data_Q.put(v)###########
                img = draw_box_text(img, data, poly_boxes)
                data = data[0]
                # save anno img
                path = os.path.join(SAVE_PATH, "anno", f"{data}")
                if not os.path.isdir(path): os.mkdir(path)
                path = os.path.join(path, f"{time_str}.jpg")
                cv2.imwrite(path, img)
                logger.info(f"Processing Time : {time.time()-start_time:.4f}")
            
            self.image_Q.put(img)
            self.data_Q.put(data) #########
            self.db_Q.put([data, path])
        
    except Exception as e:
        logger.error(f"[process]{e}")
        self.write_sys_msg(e)
        self.stop_signal = True
