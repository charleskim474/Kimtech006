
import sqlite3

class MLMSystem:
    def __init__(self):
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name1 TEXT, name2 TEXT, uname TEXT, tel TEXT, email TEXT, password TEXT,  rec_id INTEGER, acc_bal INTEGER DEFAULT 0 , FOREIGN KEY (rec_id) REFERENCES members(id))""")
        conn.commit()
        conn.close()
        
    def add_member(self, name1, name2, uname, tel, email, password, rec_id=None):
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO members(name1, name2, uname, tel, email, password, rec_id) VALUES (?, ?,?, ?, ?, ?, ?)""", (name1, name2, uname, tel, email, password, rec_id))
        conn.commit()
        conn.close()
        self.bonus_check(rec_id)
        
        
    def field_selector(self, field, value):
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM  members WHERE {field} = ?", (value,))
        data= cursor.fetchall()
        conn.close()
        return data
        
        
    def select_all(self, uname):
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        query=""" WITH RECURSIVE member_h AS (
        SELECT id, uname, rec_id
        FROM members WHERE uname = ?
        UNION ALL
        SELECT m.id, m.uname, m.rec_id FROM members m
        JOIN member_h mh ON m.rec_id = mh.id
        )
        SELECT id, uname, rec_id FROM member_h"""
        cursor.execute(query, (uname,))
        data=cursor.fetchall()
        conn.close()
        return data
        
        
    def calculator(self, uname):
        data = self.select_all(uname)
        sum=-1
        bonus=-1
        for d in data:
            sum+=1
            if sum%3 == 0:
                bonus+=1
        result=[sum, bonus]
        return result
        
        
   # FOR SEARCH
    def search_member(self, uname):
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        query=""" WITH RECURSIVE member_h AS (
        SELECT id, name1, name2, uname, tel, email, password, rec_id, acc_bal
        FROM members WHERE uname = ?
        UNION ALL
        SELECT m.id, m.name1, m.name2, m.uname, m.tel, m.email, m.password, m.rec_id, m.acc_bal FROM members m
        JOIN member_h mh ON m.rec_id = mh.id
        )
        SELECT id, name1, name2, uname, tel, email, password, rec_id, acc_bal FROM member_h"""
        cursor.execute(query, (uname,))
        data=cursor.fetchall()
        conn.close()
        return data
        
    def account(self, rec_id):
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        query="""SELECT * FROM members WHERE id= ?"""
        cursor.execute(query, (rec_id,))
        rec= cursor.fetchall()
        conn.close()
        
        if rec:
            conn = sqlite3.connect('mlm_system.db')
            cursor = conn.cursor()
            query2="""SELECT acc_bal FROM members WHERE id=?"""
            cursor.execute(query2, (rec_id,))
            bal= cursor.fetchone()
            bal=int(bal[0])
            bal = bal+10000
            query3="""UPDATE members SET acc_bal = ? WHERE id=?"""
            cursor.execute(query3, (bal, rec_id))
            conn.commit()
            conn.close()
        
        
    # bonus Check
    def bonus_check(self, rec_id):
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT uname FROM members WHERE id = ?""", (rec_id,))
        data=cursor.fetchall()
        uname=None
        for d in data:
            uname = d[0]
        total = self.calculator(uname)
        sum= total[0]
        if sum%3 == 0:
            self.bonus_adder(rec_id)
        else:
            return
            
    def bonus_adder(self, rec_id):
        if rec_id != None:
            conn = sqlite3.connect('mlm_system.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT id, rec_id, acc_bal FROM members WHERE id = ?""", (rec_id,))
            recruiter = cursor.fetchall()
            for r in recruiter:
                new_bal = r[2]+3000
                cursor.execute("""UPDATE members SET acc_bal = ? WHERE id = ?""", (new_bal,int(r[0]) ))
                conn.commit()
                conn.close()
                self.bonus_adder(r[1])
        else:
            return