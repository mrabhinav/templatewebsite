import email
from datetime import datetime
from datetime import date
from pickle import FALSE
from passlib.hash import sha256_crypt
from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3
from flask_mail import Mail
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from email.mime.text import MIMEText
import random
app = Flask (__name__)
app.config["SECRET_KEY"] = "1234"
app.config["MAIL_SERVER"] = "smtp.fastmail.com"
app.config["MAIL_PORT"] = 465
SMTP_USERNAME = "templatewebsite@fastmail.com"
SMTP_PASSWORD = "7jpmf3nn78e5cmau"
app.config["MAIL_USE_TLS"] = FALSE
app.config["MAIL_USE_SSL"] = True
sender_email = "templatewebsite@fastmail.com"
sender_password = "7jpmf3nn78e5cmau"
mail = Mail(app)


#Home Page
@app.route('/')
@app.route('/home')
def home():
    return render_template ("index.html")

#Search on Leaderbaord (username)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search = request.form.get("searchbar")
        search = "%" + search + "%"
        conn = sqlite3.connect("boats.db")
        cur = conn.cursor()
        cur.execute ("""SELECT boatid, boatname, boatcompany, departurecity, destination, capacity FROM boats WHERE destination like ?;""", [search])
        # cur.execute ("""SELECT iddonation, user.username, donated, firstname, lastname, row_number() OVER(ORDER BY donated DESC) 
        # rownumber FROM user JOIN userdonation ON user.username = userdonation.username WHERE userdonation.username like ?;""", [search])
        searchrecords = cur.fetchall()
        print(searchrecords)
        return render_template("searchresults.html", searchrecords = searchrecords)

@app.route('/bookboat/<boatid>', methods=['GET', 'POST'])
def bookboat(boatid):
    if request.method == "GET":
        if session.get("logged") == True:
            conn = sqlite3.connect("boats.db")
            cur = conn.cursor()
            cur.execute ("""SELECT capacity FROM boats WHERE boatid = ?;""", [boatid])
            capacity = cur.fetchone()
            capacity = capacity[0]
            session["boatid"] = boatid
            return render_template ("bookboat.html", capacity = capacity)
        else:
            return redirect ('/signup', message = "Please sign in before you book your ticket")
    else:
        if session.get("logged") == True:
            date = request.form.get ("date")
            time = request.form.get ("time")
            
            usercapacity = request.form.get ("usercapacity")
            boatsid = session.get ("boatid")
            conn = sqlite3.connect("boats.db")
            cur = conn.cursor()
            cur.execute ("""SELECT capacity FROM boats WHERE boatid = ?;""", [boatsid])
            capacity = cur.fetchone()
            capacity = capacity[0]
            if int(capacity) >= int(usercapacity):
                newcapacity = int(capacity) - int(usercapacity)
                print(newcapacity)
                print(boatsid)
                cur.execute ("UPDATE boats SET capacity = ? WHERE boatid = ?;", [newcapacity, boatsid])
                conn.commit()
                cur.execute ("SELECT firstname, lastname FROM user WHERE email = ?;", [session.get("email")])
                records = cur.fetchone()
                fullname = records[0] + " " + records[1]
                # cur.execute ("SELECT firstname, lastname FROM user WHERE email = ?;", [email])
                # name = cur.fetchall()
                # fullname = name[0] + " " + name[1]
                email = session.get("email")
                print(fullname)
                cur.execute ("""SELECT destination FROM boats WHERE boatid = ?;""", [boatsid])
                destination = cur.fetchone()
                destination = destination[0]
                subject = "Boat Booking Successful!"
                message = """
                Hello {},


                You have successfully booked your boat. The boat you have booked will leave on {} at {}. Your destination is {}. 
                You have booked {} seats. ENJOY!


                Sincerly,
                BOATS TEAM
                """.format(fullname, date, time, destination, usercapacity)
                sendemail(subject, email, message)
                session["boatid"] = None
                conn.close()

                return redirect ("/bookingsuccessful")
            else:
                return render_template ("/bookboat/<boatid>", message = "Not enough seats are available")
        else:
            return redirect ('/signup', message = "Please sign in before you book your ticket")

@app.route('/bookingsuccessful', methods=['GET', 'POST'])
def bookingsuccessful():
    return render_template ("bookingsuccessful.html")

@app.route('/addlisting', methods=['GET', 'POST'])
def addlisting():
    if session.get("logged") == True:
            if request.method == "GET":
                return render_template ("addlisting.html")   
            else:
                boatname = request.form.get("boatname")
                boatcompany = request.form.get("co")
                departure = request.form.get("dept")
                destination = request.form.get("dest")
                insurance = request.form.get ("insurance")
                serialnumber = request.form.get("sn")
                capacity = request.form.get("capacity")
                conn = sqlite3.connect ("boats.db")
                cur = conn.cursor()
                cur.execute("""INSERT INTO boats (boatname, boatcompany, departurecity,
                destination, capacity) VALUES (?, ?, ?, ?, ?);""", [boatname, boatcompany, departure, destination, capacity])
                conn.commit()
                conn.close()
                return render_template ("boatinformationsubmited.html")
    else:
        return redirect ("/signin")             

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "GET":
            return render_template ("signin.html")
    else:
        email = request.form.get ("email")
        password = request.form.get ("password")
        message = ""
        conn = sqlite3.connect ("boats.db")
        cur = conn.cursor()
        password_db = cur.execute ("SELECT password FROM user where email = ?;", [email]) .fetchone()
        checkpassword = sha256_crypt.verify (password, password_db[0])
        if checkpassword:
            session["email"] = email
            message  = "Login Successful"
            session["logged"] = True
            flash("Login was Sucessful", "error")
            return redirect ("/home")
        else:
            message = "Login NOT Successful"
            flash("Login was NOT Sucessful", "error")
            return render_template ("signin.html", message = message)


@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == "GET":
        return render_template ("createaccount.html")
    else:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        password = sha256_crypt.encrypt(password)
        confirmpassword = request.form.get("confirmpassword")
        message = ""
        if sha256_crypt.verify(confirmpassword, password):
            conn = sqlite3.connect("boats.db")
            cur = conn.cursor()
            cur.execute ("SELECT email FROM user WHERE email = ?;", [email])
            emailcheck = cur.fetchone()
            if emailcheck != None:
                return render_template ("createaccount.html", message = "Email already used")
            session["user"] = True
            cur.execute ("""INSERT INTO user(firstname, lastname, email, password) 
            values (?,?,?,?);""",(firstname, lastname, email,password))
            conn.commit()
            user_id = cur.execute("SELECT id FROM user WHERE email = ?;", [email]).fetchone()
            user_id = user_id[0]
            status = 0
            session["user_id"] = user_id
            # cur.execute ("INSERT INTO verfication (status, user_id) VALUES (?,?);", [status, user_id])
            conn.commit()
            conn.close()
            return render_template ("index.html", message = "Account Created")
        else:
            message = "Passwords do not match"
            return render_template("createaccount.html", message = "Sign Up Failed")
            # message = "Password not long enough"
            # return render_template("createaccount.html", message = message)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session["logged"] = False
    session.clear()
    return redirect ("/home")


@app.route('/account', methods=['GET', 'POST'])
def account():
    if session.get("logged"):
        conn = sqlite3.connect("boats.db")
        cur = conn.cursor()
        cur.execute ("SELECT email, firstname, lastname FROM user WHERE email = ?;", [session.get("email")])
        records = cur.fetchone()
        fullname = records[1] + " " + records[2]
        email = session.get("email")
        print(email)
        return render_template ("account.html", fullname = fullname, email = email)
    else:
        return render_template ("notlogged.html")

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == "GET":
        return render_template ("forgotpassword.html")
    else:
        email = request.form.get ("emailrecover")
        session["passwordrecovery"] = email
        vcode = random.randrange (1111, 9999)
        session["vcode"] = vcode
        subject = "Reset Password"
        message = """Hello, This email is sent to verify that you are changing your password on our website. Your verfication code is {}. 
        Type this code on the website to verfiy that you want to change your password. If this is not you please ignore the 
        verifcation code. Thank you!
        """.format(vcode)
        sendemail(subject, email, message)
        return redirect ("/userverfication")

@app.route('/userverfication', methods=['GET', 'POST'])
def verfication():
    if request.method == "GET":
        return render_template ("verfication.html")
    else:
        message = ""
        print("hello")
        uservcode = request.form.get ("uservcode")
        vcode = session.get("vcode")
        print(uservcode)
        print(vcode)
        if int(uservcode) == int(vcode):
            print("code was correct")
            return render_template ("passwordreset.html")
        else:
            message = "Wrong Verfication Code"
            return render_template ("verfication.html", message = message)

@app.route('/passwordreset', methods=['GET', 'POST'])
def passwordreset():
    if request.method == "GET":
        return render_template ("passwordreset.html")
    else:
        resetpassword = request.form.get ("resetpassword")
        resetpassword = sha256_crypt.encrypt(resetpassword)
        confirmpassword = request.form.get("confirmresetpassword")
        message = ""
        if sha256_crypt.verify(confirmpassword, resetpassword):
            conn = sqlite3.connect("boats.db")
            cur = conn.cursor()
            email = session.get("passwordrecovery")
            cur.execute ("UPDATE user SET password = ? WHERE email = ?;", [resetpassword, email])
            conn.commit()
            session["passwordrecovery"] = None
            return redirect ("/passwordreseted")
        else:
            return render_template ("passwordreset.html", message = "Passwords did not match")

@app.route('/passwordreseted', methods=['GET', 'POST'])
def passwordreseted():
    return render_template ("passwordreseted.html")       

def sendemail(subject, recepient_email, message):
    email_message = MIMEMultipart("alternative")
    email_message["subject"] = subject
    email_message["from"] = sender_email
    email_message["to"] = recepient_email
    part1 = MIMEText(message, "plain")
    email_message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.fastmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password  )
        server.sendmail(
        sender_email, recepient_email, email_message.as_string()
        )


@app.errorhandler(404)
def pagenotfound(e):
    return render_template ("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)


