__author__ = 'William'

import sqlite3
import os, binascii
from flask import g
import datetime

now = datetime.datetime.now()

def connect_db():
    return sqlite3.connect("/Users/William/PycharmProjects/TDDD97/database.db")

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db

def init():
    c = get_db()
    c.execute("CREATE TABLE IF NOT EXISTS "
              "'members'(email VARCHAR NOT NULL, "
              "password VARCHAR NOT NULL, "
              "first_name VARCHAR NOT NULL, "
              "family_name VARCHAR NOT NULL, "
              "gender VARCHAR NOT NULL, "
              "city VARCHAR NOT NULL,"
              "country VARCHAR NOT NULL, "
              "token VARCHAR NOT NULL)")
    c.commit()
    c1 = get_db()
    c1.execute("CREATE TABLE IF NOT EXISTS "
               "'messages'(email VARCHAR NOT NULL,"
               "message VARCHAR NOT NULL)")
    c1.commit()

def checkIfLoggedIn(email):

    c = get_db()
    cursor = c.cursor()
    cursor.execute("SELECT token FROM members WHERE email= ?", (email,))
    dbToken = cursor.fetchone()[0]

    print dbToken
    return dbToken

def signin(email, password):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("SELECT password FROM members WHERE email= ?", (email,))
    dbPass = cursor.fetchone()[0]
    if dbPass == password:
        token = binascii.b2a_hex(os.urandom(15))
        c.execute("UPDATE members SET token = ? WHERE email= ?", (token,email))
        c.commit()
        return token
    else:
        return "Error"


def signup(email, password, first, family, gender, city, country):
    c = c1 = get_db()
    cursor = c.cursor()
    token = "null"
    cursor.execute("SELECT COUNT(*) FROM members WHERE email=?",(email,))
    if (cursor.fetchone()[0]==0):
        try:
            c.execute("INSERT INTO members VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (email, password, first, family, gender, city, country, token))
            c.commit()
            print email
            c1.execute("INSERT INTO visitors VALUES(?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)", (email,))
            c1.commit()
            return "Success"
        except:
            return "Error"
    else:
        return "Exist"



def signout(email):
    c = get_db()
    c.execute("UPDATE members SET token = 'null' WHERE email=?", (email,))
    c.commit()
    if cursor.rowcount==1:
        return "Success"
    else:
        return "Error"

def changepassword(token, oldpass, newpass):
    c = get_db()
    cursor1 = cursor2 = c.cursor()
    cursor1.execute("SELECT COUNT(*) FROM members WHERE token=?",(token,))

    if(cursor1.fetchone()[0]==0):
        return "NotLoggedIn"
    else:

        cursor2.execute("SELECT COUNT(*) FROM members WHERE password=?", (oldpass,))
        if(cursor2.fetchone()[0]==0):
            return "False"
        else:
            c.execute("UPDATE members SET password=? WHERE token=?", (newpass, token))
            c.commit()
            return "Success"


def getuserdatabytoken(token):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("SELECT email, first_name, family_name, gender, city, country FROM members WHERE token=?", (token,))
    result = cursor.fetchone()
    if(result!=None):
        return result
    else:
        return "Error"

def getuserdatabyemail(email):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("SELECT email, first_name, family_name, gender, city, country FROM members WHERE email=?",(email,))
    result = cursor.fetchone()
    if(result!=None):
        addView(email)
        return result
    else:
        return "Error"

def addView(email):
    c = get_db()
    monthNum =  now.month

    if monthNum == 1:
        c.execute("UPDATE visitors SET jan = jan+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 2:
        c.execute("UPDATE visitors SET feb = feb+20 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 3:
        c.execute("UPDATE visitors SET mar = mar+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 4:
        c.execute("UPDATE visitors SET apr = apr+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 5:
        c.execute("UPDATE visitors SET may = may+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 6:
        c.execute("UPDATE visitors SET jun = jun+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 7:
        c.execute("UPDATE visitors SET jul = jul+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 8:
        c.execute("UPDATE visitors SET aug = aug+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 9:
        c.execute("UPDATE visitors SET sep = sep+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 10:
        c.execute("UPDATE visitors SET oct = oct+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 11:
        c.execute("UPDATE visitors SET nov = nov+1 WHERE email=?", (email,))
        c.commit()
    elif monthNum == 12:
        c.execute("UPDATE visitors SET dec = dec+1 WHERE email=?", (email,))
        c.commit()


def postmessage(email, message):
    c = get_db()
    try:
        c.execute("INSERT INTO messages VALUES (?,?)", (email, message))
        c.commit()
        return "Success"
    except:
        return "Error"

def getmessagebytoken(token):
    c = get_db()
    usercursor = c.cursor()
    usercursor.execute("SELECT email FROM members WHERE token=?", (token,))
    userEmail= usercursor.fetchone()[0]
    if(userEmail==None):
        return "Error"
    else:
        return getmessagebyemail(userEmail)

def getmessagebyemail(email):
    c = get_db()
    messagecursor = c.cursor()
    messagecursor.execute("SELECT message FROM messages WHERE email=?", (email,))
    messages = messagecursor.fetchall()
    if(messages==None):
        return "Error"
    else:
        return messages

def getVisitors(email):
    c = get_db()
    visitorCursor = c.cursor()
    visitorCursor.execute("SELECT * FROM visitors WHERE email=?", (email,))
    visitors = visitorCursor.fetchall()
    return visitors