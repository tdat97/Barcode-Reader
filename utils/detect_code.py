from utils.logger import logger
from utils.tool import get_poly_box_wh, crop_obj_in_bg
from pyzbar.pyzbar import ZBarSymbol
from pyzbar import pyzbar
import cv2
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
import os

# DBSCAN
EPS = 0.04
MinSamples = 30

# filter
RATIO = 4

######################################################################
def get_qrcode(img):
    detect = pyzbar.decode(img, symbols=[ZBarSymbol.QRCODE])
    data = [det.data.decode('utf-8') for det in detect]
    poly_boxes = [np.array(det.polygon) for det in detect]
    
    return data, poly_boxes

######################################################################
def find_barcode(img_gray):
    mser = cv2.MSER_create()
    mser.setMinArea(min(img_gray.shape[:2])//20)
    mser.setMaxArea(min(img_gray.shape[:2])*3)

    img_h, img_w = img_gray.shape[:2]
    regions, _ = mser.detectRegions(img_gray)
    if not regions:
        logger.debug("Not found regions.")
        return [], None

    # polygon을 사각형으로 만들고 비율 필터링 (바코드의 검은색 바 찾기)
    rectes = [cv2.minAreaRect(p) for p in regions]
    rectes = list(filter(lambda x:max(x[1]) > RATIO*min(x[1]), rectes))
    boxes = np.array([cv2.boxPoints(rect).astype(np.int32) for rect in rectes])
    if not rectes:
        logger.debug("Not found long boxes.")
        return [], None

    center_x = [rect[0][0] for rect in rectes]
    center_y = [rect[0][1] for rect in rectes]
    # theta = [rect[2] for rect in rectes]
    height = [max(rect[1]) for rect in rectes]
    X = np.stack([center_x, center_y, height], axis=1)
    X[:, 0] /= img_w
    X[:, 1] /= img_h
    X[:, 2] /= np.mean(height)

    # 밀집된 구역 찾기
    dbscan = DBSCAN(eps=EPS, min_samples=MinSamples).fit(X)
    cluster_idx = dbscan.labels_
    kind_idx, kind_counts = np.unique(cluster_idx, return_counts=True)
    logger.debug(f"kind_idx : {kind_idx}, kind_counts : {kind_counts}")

    # debug
    debug_img = np.tile(img_gray.copy()[...,None], (1,1,3))
    colors = [tuple(map(int, np.random.randint(50, 200, size=3)))
              for _ in range(len(kind_idx))]

    for box, i in zip(boxes, cluster_idx):
        color = (255,255,255) if i == -1 else colors[i]
        cv2.polylines(debug_img, [box], True, color)
    
    # 바코드 박싱
    barcode_boxes = []
    for kind in kind_idx:
        if kind == -1: continue
        kind_boxes = boxes[np.where(cluster_idx==kind)]
        points = kind_boxes.reshape(-1, 2) # (n, 4, 2) -> (m, 2)
        # ((a,b),(c,d),e) -> [(a,b), ndarr(c,d), e]
        big_rect = list(cv2.minAreaRect(points))
        big_rect[1] = np.array(big_rect[1]) * 1.2
    
        barcode_box = cv2.boxPoints(big_rect).astype(np.int32)
        barcode_boxes.append(barcode_box)
        
    # debug2
    for box in barcode_boxes:
        color = (0,0,255)
        cv2.polylines(debug_img, [box], True, color)

    return barcode_boxes, debug_img
    

def get_barcode(img):
    img = img.squeeze()
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
        
    barcode_boxes, debug_img = find_barcode(img_gray)
    if not barcode_boxes:
        logger.debug(f"Not found barcode_boxes")
        return [], [], None

    barcode_imgs = []
    for poly_box in barcode_boxes:
        w, h = get_poly_box_wh(poly_box)
        barcode_img, _ = crop_obj_in_bg(img, poly_box, w, h)
        barcode_imgs.append(barcode_img)
        
    data = []
    boxes = []
    for img, box in zip(barcode_imgs, barcode_boxes):
        detect = pyzbar.decode(img)
        if not detect:
            logger.debug("Candidate img could not be decode..")
            continue
        data.append(detect[0].data.decode('utf-8'))
        boxes.append(box)

    if len(data) != len(barcode_imgs):
        msg = f"Candidate : {len(barcode_imgs)}, Decodable : {len(data)}"
        logger.warning(msg)

    return data, boxes, debug_img

######################################################################
def draw_box_text(img, data, poly_boxes):
    img = img.copy()
    for text, poly in zip(data, poly_boxes):
        cv2.polylines(img, [poly], True, (255,0,0))
        text_loc = np.min(poly, axis=0)
        text_loc[1] -= 10
        cv2.putText(img, text, text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    return img
    










    
    
