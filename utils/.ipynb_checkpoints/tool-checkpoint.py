import numpy as np
import cv2
import datetime


def get_poly_box_wh(poly_box): # (4,2)
    lt, rt, rb, lb = poly_box
    w = int((np.linalg.norm(lt - rt) + np.linalg.norm(lb - rb)) // 2)
    h = int((np.linalg.norm(lt - lb) + np.linalg.norm(rt - rb)) // 2)
    return w, h


def crop_obj_in_bg(bg_img, poly, w, h):
    poly = poly.astype(np.float32)
    pos = np.float32([[0,0], [w,0], [w,h], [0,h]])
    M = cv2.getPerspectiveTransform(poly, pos)
    obj_img = cv2.warpPerspective(bg_img, M, (w, h))
    return obj_img, M

def get_time_str(human_mode=False):
    now = datetime.datetime.now()
    if human_mode:
        s = f"{now.year:04d}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}:{now.second:02d}"
    else:
        s = f"{now.year:04d}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}"
        s += f"_{now.microsecond:06d}"
    return s

def fix_ratio_resize_img(img, size, target='w'):
    h, w = img.shape[:2]
    ratio = h/w
    if target == 'w': resized_img = cv2.resize(img, dsize=(size, int(ratio * size)))
    else:             resized_img = cv2.resize(img, dsize=(int(size / ratio), size))
    return resized_img

def clear_Q(Q):
    with Q.mutex:
        Q.queue.clear()
        
def clear_serial(ser):
    while True:
        if ser.read_all() == b'': break