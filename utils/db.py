from utils.logger import logger
from collections import defaultdict, Counter
import pymysql
import json
import time
import os

DB_INFO_PATH = "./temp/db.json"



def connect_db():
    with open(DB_INFO_PATH, 'r', encoding='utf-8') as f:
        info_dic = json.load(f)
    con = pymysql.connect(**info_dic, charset='utf8', autocommit=True, cursorclass=pymysql.cursors.Cursor)
    cur = con.cursor()
    return con, cur

def load_db(self):
    # 코드,이름 쌍 가져오기
    sql = "SELECT code, name from Product_list;" # 둘 다 NOT NULL
    self.cursor.execute(sql)
    rows = self.cursor.fetchall()
    code2name = dict(rows)
    
    # 오늘날짜들 가져오기
    sql = "SELECT code from Image_stack WHERE date > curdate();"
    self.cursor.execute(sql)
    rows = self.cursor.fetchall()
    rows = list(map(lambda x:x[0], rows))
    code2cnt = defaultdict(int, Counter(rows))

    return code2name, code2cnt
    

def db_process(self):
    try:
        while True:
            time.sleep(0.1)
            if self.stop_signal: break
            if self.db_Q.empty(): continue

            code, path = self.db_Q.get()
            path = os.path.realpath(path).replace('\\','/')
            
            # Image_stack에 이미지 경로 추가
            sql = f"INSERT INTO Image_stack(code, path) VALUES ('{code}', '{path}')"
            if code is None:
                sql = f"INSERT INTO Image_stack(path) VALUES ('{path}')"
            self.cursor.execute(sql)

    except Exception as e:
        logger.error(f"[db_process] {e}")
        self.write_sys_msg(e)
        self.stop_signal = True