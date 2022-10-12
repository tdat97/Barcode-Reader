from utils.logger import logger
from collections import defaultdict
import pymysql
import json
import time

DB_INFO_PATH = "./temp/db.json"

def connect_db():
    with open(DB_INFO_PATH, 'r', encoding='utf-8') as f:
        info_dic = json.load(f)
    con = pymysql.connect(**info_dic, charset='utf8', autocommit=True, cursorclass=pymysql.cursors.Cursor)
    cur = con.cursor()
    return con, cur

def load_db(self):
    # init
    sql = "UPDATE Summary_cnt SET total = 0;"
    self.cursor.execute(sql)
    sql = "UPDATE Summary_cnt SET total_ok = 0;"
    self.cursor.execute(sql)
    sql = "UPDATE Summary_cnt SET total_fail = 0;"
    self.cursor.execute(sql)
    sql = "UPDATE Product SET cnt = 0;"
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
                
                ###################################################### Summary_cnt
                cols = ["stack_total", "total", "stack_total_ok", "total_ok"]
                if code is None:
                    cols[2] = "stack_total_fail"
                    cols[3] = "total_fail"
                
                formulas = list(map(lambda x:f"{x}={x}+1"))
                text = ', '.join(formulas)
                
                # 1씩 더하기
                sql = f"UPDATE Product SET {text};"
                self.cursor.execute(sql)
                
                ###################################################### Product
                # 코드가 db에 없을 경우
                sql = "SELECT code from Product;"
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                if not rows:
                    sql = f"INSERT INTO Product(code) VALUES ('{code}');"
                    self.cursor.execute(sql)
                
                # 1씩 더하기
                sql = f"UPDATE Product SET stack_cnt=stack_cnt+1, cnt=cnt+1 where code={code};"
                self.cursor.execute(sql)
                
                ###################################################### Image_stack
                path = os.path.realpath(path)
                sql = f"INSERT INTO Image_stack(pcode, path) VALUES ({code}, {path})"
                
    except Exception as e:
        logger.error(f"[db_process] {e}")
        self.msg_label.configure(text=e)
        self.stop_signal = True
            
            