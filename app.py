import sqlite3
import datetime
from flask import Flask, request,  render_template, redirect, url_for, session
from mlmsystem import MLMSystem
from forms import Registration, Login


app=Flask('__name__')
app.config['SECRET_KEY']='68uhf66uh678ijj6'

mlm = MLMSystem()
t_bal=0

#Login_________________________     
        
@app.route('/', methods=['POST', 'GET'])
def login():
    form=Login()
    uname=form.uname.data
    
    session['uname']=uname
    
    pw=form.password.data
    conn = sqlite3.connect('mlm_system.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM members WHERE uname=?""", (uname,))
    member= cursor.fetchone()
    if member:
        if member[6]==pw:
            return redirect(url_for('home', uname=uname)) 
        else:
            e=1
            return render_template('index.html', form=form, e=e)
    else:
        return render_template('index.html', form=form )
        

#Registration______,,,____________

@app.route('/register', methods=['POST', 'GET'])
def add_member():
    form=Registration()
    if form.validate_on_submit():
        name1=form.name1.data
        name2=form.name2.data
        tel=form.tel.data
        email=form.email.data
        password=form.password.data
        rec_id=form.rec_id.data
        un=mlm.field_selector('uname', form.uname.data)
        if un:
            un=1
            return render_template('register.html', form=form, un=un)
            
        else:
            uname=form.uname.data
            session['uname']=uname
            
            if rec_id:
                int(rec_id)
                mlm.account(rec_id)
                mlm.add_member(name1, name2, uname, tel, email, password, rec_id)
                return redirect(url_for('home',  name=form.uname.data))
            else:
                mlm.add_member(name1, name2, uname, tel, email, password)
                return redirect(url_for('home',  name=form.uname.data))

    else:
        return render_template('register.html', form=form)
       
#Home page_____________________
    
    
@app.route('/home')
def home():
    n= datetime.datetime.now()
    y=str(n.year)
    m=str(n.month)
    d=str(n.day)
    h=str(n.hour)
    min=str(n.minute)
    time=d+'/'+m+'/'+y+'-'+h+' : '+min

    uname=session.get('uname')
    recruits=mlm.select_all(uname)
    total=mlm.calculator(uname)
    
    myId=recruits[0]
    conn = sqlite3.connect('mlm_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT acc_bal FROM members WHERE uname=?", (uname,))
    bal=cursor.fetchall()
    
    return render_template('home.html', recruits=recruits, total= total, uname=uname, myId=myId, bal= bal[0])
    
    
#ADMINISTRATION SECTION________    
    
@app.route('/admin_index', methods=['POST', 'GET'])
def admin():
    uname = request.form.get('uname')
    pw= request.form.get('pw')
    if uname=='Kimtech006' and pw=='kimtech.com':
        conn = sqlite3.connect('mlm_system.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM members""")
        members=cursor.fetchall()
        conn.close()
        
        total=0
        t_bal=0
        for m in members:
            total = total+1
            t_bal+=m[8]
            
        return render_template('admin_home.html', total=total, t_bal = t_bal )
    return render_template('admin_index.html')


@app.route('/members')
def members():
    conn = sqlite3.connect('mlm_system.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM members""")
    members=cursor.fetchall()
    conn.close()
    sum=0
    t_bal=0
    for m in members:
        t_bal+=m[8]
        sum+=1
    return render_template('members.html', members=members, sum=sum, t_bal=t_bal )
    
    
@app.route('/search', methods=['POST', 'GET'])
def support():
    uname = request.form.get('uname')
    if uname:
        result = mlm.search_member(uname)
        sum= mlm.calculator(uname)
        
        return render_template('search.html', results=result, sum=sum, t_bal=t_bal )
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)