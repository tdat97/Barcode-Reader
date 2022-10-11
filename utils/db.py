from utils.logger import logger
import pymysql
import json

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
    
    sql = "SELECT name, code from Product;"
    self.cursor.execute(sql)
    rows = self.cursor.fetchall()
    name2code = dict(rows)
    code2name = dict(zip(name2code.values(), name2code.keys()))
    
    sql = "SELECT name, stack_cnt from Product;"
    self.cursor.execute(sql)
    rows = self.cursor.fetchall()
    name2stack_cnt = dict(rows)

    return name2code, code2name, name2stack_cnt
    

def db_process(self):
    pass