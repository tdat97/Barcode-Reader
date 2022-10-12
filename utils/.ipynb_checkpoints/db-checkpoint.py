from utils.logger import logger
from collections import defaultdict
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
    # init
    sql = "UPDATE Summary_cnt SET current_total = 0;"
    self.cursor.execute(sql)
    sql = "UPDATE Summary_cnt SET current_total_ok = 0;"
    self.cursor.execute(sql)
    sql = "UPDATE Summary_cnt SET current_total_fail = 0;"
    self.cursor.execute(sql)
    sql = "UPDATE Product SET current_cnt = 0;"
    self.cursor.execute(sql)
    
    sql = "SELECT code, name from Product;"
    self.cursor.execute(sql)
    rows = self.cursor.fetchall()
    code2name = dict(rows)
    
    sql = "SELECT code, stack_cnt from Product;"
    self.cursor.execute(sql)
    rows = self.cursor.fetchall()
    code2stack_cnt = defaultdict(int, dict(rows))

    return code2name, code2stack_cnt
    

def db_process(self):
    try:
        while True:
            time.sleep(0.1)
            if self.stop_signal: break
            if self.db_Q.empty(): continue

            code, path = self.db_Q.get()
            path = os.path.realpath(path).replace('\\','/')

            ###################################################### Summary_cnt         
            cols = ["stack_total", "current_total", "stack_total_ok", "current_total_ok", ]
            if code is None: cols[2:4] = ["stack_total_fail", "current_total_fail", ]
            
            formulas = list(map(lambda x:f"{x}={x}+1", cols))
            text = ', '.join(formulas)
            # 1씩 더하기
            sql = f"UPDATE Summary_cnt SET {text};"
            self.cursor.execute(sql)
            
            ###################################################### Product
            # 코드가 db에 없을 경우
            if code is not None:
                sql = f"SELECT * from Product WHERE code='{code}';"
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                if not rows:
                    sql = f"INSERT INTO Product(code) VALUES ('{code}');"
                    self.cursor.execute(sql)

            # 1씩 더하기
            sql = f"UPDATE Product SET stack_cnt=stack_cnt+1, current_cnt=current_cnt+1 where code='{code}';"
            if code is None:
                sql = f"UPDATE Product SET stack_cnt=stack_cnt+1, current_cnt=current_cnt+1 where code=NULL;"
            self.cursor.execute(sql)
            
            ###################################################### Image_stack
            time.sleep(0.01)
            sql = f"INSERT INTO Image_stack(pcode, path) VALUES ('{code}', '{path}')"
            if code is None:
                sql = f"INSERT INTO Image_stack(path) VALUES ('{path}')"
            self.cursor.execute(sql)
            
                
                
    except Exception as e:
        logger.error(f"[db_process] {e}")
        self.msg_label.configure(text=e)
        self.stop_signal = True
            
            