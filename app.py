
import os
from time import time
from flask_sqlalchemy import SQLAlchemy
from requests import Session, session
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from django.shortcuts import redirect
from flask import Flask,url_for,render_template,request,flash,jsonify
from flask_mysqldb import MySQL
from tkinter import * 
from flask_migrate import Migrate
import uuid
import os
from flask_session import Session

import time
from tkinter import messagebox

import json

app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='database'
picfolder = os.path.join('static','pic')
picfolder2 = os.path.join('static','profile')
app.config['UPLOAD_FOLDER'] =picfolder
app.config['PROFILE_FOLDER'] =picfolder2

"""basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] =False
db = SQLAlchemy(app)
Migrate(app,db)
"""


mysql = MySQL(app)
#conn = mysql.connector.connect(host = "localhost",username = "root",password = "Anant@123",database = "database")
#cursor = conn.cursor()
@app.route('/missing_upload', methods=['POST','GET'])
def missing_upload():
    name = request.form.get('name')
    age = request.form.get('age')
    mob = request.form.get('mob')
    gender = request.form.get('gender')
    area = request.form.get('area')
    details = request.form.get('details')
    key = uuid.uuid1()
    img = request.files["image"]
    img.save(f"static/fir/{key}{img.filename}")
    image =str(key)+img.filename
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `missing_record` (`name`, `age`, `mob`, `gender`, `area`, `details`, `image`) VALUES (%s,%s,%s,%s,%s,%s,%s);",(name,age,mob,gender,area,details,image))
    mysql.connection.commit()
    
    return render_template('missing.html')
@app.route('/design')
def design():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM fir_record")
    data = cur.fetchall()
    cur.close()
    
    return render_template('received.html',fir_record = data)

@app.route('/fir_record' , methods=['POST','GET'])
def fir_record():
    name =  request.form.get('name')
    cname = request.form.get('cname')
    area =  request.form.get('area')

    subject = request.form.get('subject')
    subject2 = request.form.get('subject2')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `fir_record` (`name`, `cname`, `area`,  `subject`, `subject2`) VALUES (%s,%s,%s,%s,%s);",(name,cname,area,subject,subject2))
    mysql.connection.commit()
    return render_template('fir2.html')

@app.route('/requirements')

def requirements():
    return render_template('requirements.html')
@app.route('/how_to_do')
def how_to_do():
    return render_template('how_to_do.html')
@app.route('/what_to_do')
def what_to_do():
    return render_template('what_to_do.html')
@app.route('/lost')
def lost():
    return render_template('lost.html')
@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')
@app.route('/seen')
def seen():
    return render_template('seen.html')
@app.route('/missing')
def missing():
    return render_template('missing.html')
@app.route('/fir')
def fir():
    return render_template('fir.html')
@app.route("/")
def index():
    return render_template('index.html')
@app.route('/results', methods=['POST','GET'])
def results():
    if request.method == "POST":
        searched = request.form.get('search')

        count=0
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `criminal_record` WHERE `aad` = {searched}")
        DATA = cur.fetchall()
        for i in DATA:
            count+=1
      
        if count > 0:
            cur2 = mysql.connection.cursor()
            cur2.execute(f"SELECT `img_id` FROM `criminal_record` WHERE `aad` = {searched}")
            DATA2 = cur2.fetchall()
            res = str(DATA2).strip('()')
            new_res = res.replace(",","")
            res2 = new_res.replace(")","")
            res3 = res2.replace("'","")
            print(res3)
            pic1 =  os.path.join(app.config['UPLOAD_FOLDER'],res3)
            print(pic1)

            return render_template('view.html',DATA = DATA, user_img = pic1)

        else:
            return render_template('no_result.html')
@app.route('/no_result')
def no_result():
    return render_template('no_result.html')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/contact_normal')
def contact_normal():
    return render_template('contact_normal.html')
@app.route('/sucess_login')
def sucess_login():
    return render_template('sucess_login.html')
@app.route('/login')
def login__signup():
    return render_template('login__signup.html')
@app.route('/login_to',methods=['POST','GET'])
def login_to():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        code = request.form.get('code')
        
        if password == password2:
                ls = ['JSR01','JSR02']
               
                print(code)
                if code in ls:

                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO `users` ( `name`, `email`, `password`) VALUES (%s, %s, %s)",(username,email,password))
                    mysql.connection.commit()
                    provide ="ADMIN"

                    cur2 = mysql.connection.cursor()
                    cur2.execute("INSERT INTO `station_code` (`provider`, `code`) VALUES (%s,%s)",(provide,code))
                    mysql.connection.commit()
         
         
                    return render_template('sucess_login.html')
                else:
                    return render_template('wrrong2.html')
        else:
            
            return render_template('wrong3.html')
@app.route('/login_valid',methods=['POST','GET'])
def login_valid():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM  `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
        users = cur.fetchall()
        if len(users)>0:
            return render_template('home.html')

        else:
            
            return render_template('wrong_login.html')


@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/search_normal')
def search_normal():
    return render_template('search_normal.html')
@app.route('/list')
def list():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM criminal_record")
    data = cur.fetchall()
    cur.close()
    
    return render_template('list.html',criminal_record = data)

@app.route('/add')
def add():
    return render_template('add.html')
@app.route('/upload')
def upload():
    pass
@app.route('/aboutus')
def aboutus():
    pic1 = os.path.join(app.config['PROFILE_FOLDER'],'anant.jpeg')

    pic2 = os.path.join(app.config['PROFILE_FOLDER'],'vishal.jpg')
    pic3 = os.path.join(app.config['PROFILE_FOLDER'],'swasti.jpeg')
    return render_template('aboutus.html',user1 =pic1,user2 =pic2,user3 =pic3)
@app.route('/aboutus_normal')
def aboutus_normal():
    pic1 = os.path.join(app.config['PROFILE_FOLDER'],'anant.jpeg')

    pic2 = os.path.join(app.config['PROFILE_FOLDER'],'vishal.jpg')
    pic3 = os.path.join(app.config['PROFILE_FOLDER'],'swasti.jpeg')
    return render_template('aboutus_normal.html',user1 =pic1,user2 =pic2,user3 =pic3)

@app.route('/uploader',methods= ['GET','POST'])
def uploader():
    if request.method == "POST":
        name = request.form.get('name')
        gender = request.form.get('gender')
        fname = request.form.get('fname')
        addr = request.form.get('addr')
        crime = request.form.get('crime')
        cri = request.form.get('cri')
        aad = request.form.get('aad')
        mob = request.form.get('mob')
        date = request.form.get('date')
        print(mob)
        key = uuid.uuid1()
        time.sleep(5)
        key2 = uuid.uuid1()
        img = request.files["image"]
        aadhar = request.files["aadhar"]

        img.save(f"static/pic/{key}{img.filename}")
        
        aadhar.save(f"static/pic/{key2}{aadhar.filename}")

        img_id =str(key)+img.filename
        aadhar_id = str(key2)+aadhar.filename
        cur = mysql.connection.cursor()
        submitted_by= "Admin"
    
        cur.execute("INSERT INTO `criminal_record` ( `name`,`gender`,`fname`,`addr`,`crime`,`cri`,`aad`,`mob`,`date`,`img_id`,`aadhar_id`,`submitted_by`) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)",(name,gender,fname,addr,crime,cri,aad,mob,date,img_id,aadhar_id,submitted_by))
        mysql.connection.commit()
        return render_template('add.html')
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')
@app.route('/reset',methods=['GET','POST'])
def reset():

    return render_template('thankyou.html')
@app.route('/wrong_login')
def wrong_login():
    return render_template('wrong_login.html')
if __name__ == "__main__":
    app.run(debug=True)






#<img src="https://pbs.twimg.com/media/D3dQ7Y6WAAAEv8l.jpg"
"""class="miss">
                    </div>
                    <div>
                      <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5ZZ7DSSFEaPqEqrFLkqWItJo5blzYA4WGfw&usqp=CAU" class="miss">"""