from utils.logger import logger
from utils.detect_code import get_barcode, get_qrcode, draw_box_text
from gui.mainloop import VisualControl
from pyzbar.pyzbar import ZBarSymbol
from pyzbar import pyzbar
import cv2
import tkinter as tk


def run_console_mode(img_path):
    img = cv2.imread(img_path)
    path = img_path.split('/')[-1].split('\\')[-1]
    
    if img is None:
        logger.error("Invalid image path.")
        return
    
    qr_data, qr_poly = get_qrcode(img)
    if not qr_data: logger.info("QRcode is not found.")
    else:
        for qr in qr_data:
            logger.info(f"QRcode : {qr}")
    
    bar_data, bar_poly, debug_img = get_barcode(img)
    if not bar_data:
        logger.info("Barcode is not found.")            
        cv2.imwrite("./image/debug/"+path, debug_img)
        return
    else:
        for bar in bar_data:
            logger.info(f"Barcode : {bar}")
            
    img = draw_box_text(img, qr_data, qr_poly)
    img = draw_box_text(img, bar_data, bar_poly)
    cv2.imwrite("./image/anno/"+path, img)
    cv2.imwrite("./image/debug/"+path, debug_img)


def run_gui_mode():
    root = tk.Tk()
    VisualControl(root)
    root.mainloop()
