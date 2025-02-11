import sqlite3
import datetime
from flask import Flask, request,  render_template, redirect, url_for, session
from mlmsystem import MLMSystem, R_forms, Cashout
from forms import Registration, Login, Requests, Auto, Withdraw


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
    uname=session.get('uname')
    recruits=mlm.select_all(uname)
    total=mlm.calculator(uname)

    myId=recruits[0]
    conn = sqlite3.connect('mlm_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT acc_bal FROM members WHERE uname=?", (uname,))
    bal=cursor.fetchall()

    return render_template('home.html', recruits=recruits, total= total, uname=uname, myId=myId, bal= bal[0])


@app.route('/form', methods=['POST', 'GET'])
def form():
        form = Requests()
        if form.validate_on_submit():
            name1=form.name1.data
            name2=form.name2.data
            tel=form.tel.data
            email=form.email.data
            rec_id=form.rec_id.data
            password=form.pw.data
            opt=form.opt.data
            txn=form.txn.data
            req=R_forms()
            req.form(name1, name2, tel, email, rec_id, password, txn, opt)
            return render_template('form.html', msg=1)
        return render_template('form.html', msg=0, form=form)
        
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how')
def how():
    return render_template('how.html')


#ADMINISTRATION SECTION________________,,,,______

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


@app.route('/requests')
def requests():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forms ")
    data=cursor.fetchall()
    conn.close()
    return render_template('requests.html', data=data)


@app.route('/auto', methods=['POST', 'GET'])
def auto():
    form=Auto()
    if form.validate_on_submit():
        id = form.id.data
        int(id)
        uname= form.uname.data
        un = mlm.field_selector('uname', uname)
        if un:
            return render_template('auto_register.html', form=form, msg=0)
        else:
            conn = sqlite3.connect('form_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM forms WHERE id=?", (id, ))
            data = cursor.fetchall()
            conn.close()
            for d in data:
                mlm.add_member(d[1], d[2], uname, d[3], d[4], d[6], d[5])
            mlm.account(int(d[5]))
            mlm.delete(id)
            return redirect(url_for('requests'))
    return render_template('auto_register.html', form=form)



@app.route('/withdraw', methods=['POST', 'GET'])
def withdraw():
    cash=Cashout()
    form=Withdraw()
    if form.validate_on_submit():
        amm=form.amm.data
        name=form.name.data
        pw=form.pw.data
        uname= session.get('uname')
        check = mlm.field_selector('uname', uname)
        
        if pw==check[6]:
            a = int(amm)
            b = int(check[8])
            if a <= b:
            
                n= datetime.datetime.now()
                y=str(n.year)
                m=str(n.month)
                d=str(n.day)
                h=str(n.hour)
                min=str(n.minute)
                time=d+'/'+m+'/'+y+'-'+h+' : '+min
                id=check[0]
                acc_bal=check[8]
                cash.add_request(time, name, amm)
                ba=cash.new_balance( id, b, a)
            
                return render_template('withdraw.html', msg=1)
            else:
                return render_template('withdraw.html', form= form, msg=2)
                
        else:
            return render_template('withdraw.html', form= form, msg=0)
        
    return render_template('withdraw.html', form= form, msg=None)

@app.route('/pay')
def pay():
    conn = sqlite3.connect('withdraw.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM withdraw")
    req=cursor.fetchall()
    conn.close()
    return render_template('w_request.html', req=req)
    
    
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method=="POST":
        id=request.form.get('id')
        conn = sqlite3.connect('withdraw.db')
        cursor = conn.cursor()
        cursor.execute("""UPDATE withdraw SET status = "--Paid--" WHERE id = ?""", ( id, ))
        conn.commit()
        conn.close()
        return redirect(url_for('pay'))
    return render_template('confirm_pay.html')


if __name__ == '__main__':
    app.run(debug=True)