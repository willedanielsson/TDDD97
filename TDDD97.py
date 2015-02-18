from flask import Flask, url_for
from flask import request
from flask import jsonify
from flask import json
app = Flask(__name__)
from flask import render_template
import database_helper
# -*- coding: utf-8 -*-

@app.route('/')
def hello_world():
    database_helper.init()
    #return app.send_static_file('test.html')

@app.route('/test', methods=['GET'])
def test():
    print "Inne i test"
    return "Hej"

@app.route('/signin', methods=['POST'])
def sign_in():
    print "Signin in"
    email = request.form['email']
    password = request.form['password']
    response = database_helper.signin(email, password)
    print response
    json.dumps({'success' : False, 'message' : 'wrong password'})
    if response=="Error":
        return jsonify(success=False,
                       message="Wrong username or password.",)
    else:
        return jsonify(success=True,
                       message="Successfully signed in.",
                       data=response)


@app.route('/signup', methods=['POST'])
def sign_up():
    print "Signin up"

    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    familyname = request.form['familyname']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']

    if (email!="NULL" and password!="NULL" and firstname!="NULL" and familyname!="NULL" and gender!="NULL" and city!="NULL" and country!="NULL"):
        response = database_helper.signup(email, password, firstname, familyname, gender, city, country)
        if(response=="Success"):
            return jsonify(success=True,
                       message="Successfully created a new user.")
        elif(response=="Error"):
            return jsonify(success=False,
                           message="Something went wrong.")
        elif(response=="Exist"):
            return jsonify(success=False,
                       message="User already exists.")


@app.route('/signout', methods=['GET'])
def sign_out():
    print "Signing out"
    token = request.args.get('token')
    response = database_helper.signout(token)
    if(response=="Success"):
        return jsonify(success=True,
                       message="Successfully signed out.")
    else:
        return jsonify(success=False,
                       message="You are not signed in.")

@app.route('/changepassword', methods=['POST'])
def change_password():
    print "Changing pass"
    token = request.form['token']
    oldpass = request.form['oldpass']
    newpass = request.form['newpass']
    response = database_helper.changepassword(token, oldpass, newpass)
    if(response=="Success"):
        return jsonify(success=True,
                       message="Password changed.")
    elif(response=="NotLoggedIn"):
        return jsonify(success=False,
                       message="You are not logged in.")
    else:
        return jsonify(success=False,
                       message="Incorrect old password")


@app.route('/getuserdatabytoken', methods=['POST'])
def get_user_data_by_token():
    print "Getting data for user"
    token = request.form['token']
    response = database_helper.getuserdatabytoken(token)
    if response=="Error":
        return jsonify(success=False,
                       message="No such user.")
    else:
        return jsonify(success=True,
                       message="User data retrieved.",
                       #data=response[0]+", "+response[1]+", "+response[2]+", "+response[3]+", "+response[4]+", "+response[5])
                        data=response)


@app.route('/getuserdatabyemail', methods=['POST'])
def get_user_data_by_email():
    print "Getting data for friend"
    token = request.form['token']
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        email = request.form['email']
        response = database_helper.getuserdatabyemail(email)
        if(response=="Error"):
            return jsonify(success=False,
                           message="No such user.")
        else:
             return jsonify(success=True,
                           message="User data retrieved.",
                           data=response)


@app.route('/postmessage', methods=['POST'])
def post_message():
    print "Posting message"
    token = request.form['token']
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        email = request.form['email']
        userExist = database_helper.getuserdatabyemail(email)
        if(userExist=="Error"):
            return jsonify(success=False,
                           message="No such user.")
        else:
            message = request.form['message']
            response = database_helper.postmessage(email, message)
            if(response == "Success"):
                return jsonify(success=True, message="Message posted.")
            else:
                return jsonify(success=False, message="Failed to post.")

@app.route('/getusermessagebytoken', methods=['POST'])
def get_user_message_by_token():
    print "Getting message by token"
    token = request.form['token']
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        response=database_helper.getmessagebytoken(token)
        print(response)
        if(response=="Error"):
            return jsonify(success=False,
                       message="No such user")
        else:
            return jsonify(success=True,
                           message="User messages received.",
                           data=response)

@app.route('/getusermessagebyemail', methods=['POST'])
def get_user_message_by_email():
    print "Getting message by email"
    token = request.form['token']
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        email = request.form['email']
        response=database_helper.getmessagebyemail(email)
        if(response=="Error"):
            return jsonify(success=False,
                       message="No such user")
        else:
            return jsonify(success=True,
                           message="User messages received.",
                           data=response)


if __name__ == '__main__':
    app.run(debug=True)