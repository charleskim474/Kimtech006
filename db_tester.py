#tester
import sqlite3
from mlmsystem import MLMSystem
mlm=MLMSystem()

#DB CONTENTS_____________
conn = sqlite3.connect('mlm_system.db')
cursor = conn.cursor()
query="SELECT * FROM members"


uery=""" WITH RECURSIVE member_h AS (
        SELECT id, uname, rec_id
        FROM members WHERE uname = ?
        UNION ALL
        SELECT m.id, m.uname, m.rec_id FROM members m
        JOIN member_h mh ON m.rec_id = mh.id
        )
        SELECT id, uname, rec_id FROM member_h"""

value='u7'
cursor.execute(query)
data=cursor.fetchall()
for d in data:
    print("=>")
    print(d)
    
#RECRUITS______________
    
x="""id=1
data=mlm.select_all(id)
for d in data:
    print(d)"""
    
    
#BONUS CALCULATOR_________
x="""dd=mlm.calculator(1)
for d in dd:
    print(d)"""