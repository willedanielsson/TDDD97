from flask import Flask
from flask import request
from flask import jsonify
from flask import json
app = Flask(__name__)
import gevent
from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import database_helper
# -*- coding: utf-8 -*-

connectedWS = []

@app.route('/')
def hello_world():
    database_helper.init()
    return app.send_static_file('client.html')


@app.route('/signin', methods=['POST'])
def sign_in():
    print "Loggin in"
    email = request.form['email']
    # Send the email to every other logged in users. They will check if it is their email and then be logged-off
    userToken = database_helper.checkIfLoggedIn(email)
    if(userToken!="null"):
        replaced = True
        data = json.dumps({'token': userToken,
                       'action':"sign"})

        for ws in connectedWS:
            ws.send(data)
    else:
        replaced=False

    password = request.form['password']
    response = database_helper.signin(email, password)
    json.dumps({'success' : False, 'message' : 'wrong password'})
    if response=="Error":
        return jsonify(success=False,
                       message="Wrong username or password.",)
    else:
        # If the new logged in replaced an already logged in user, there is no change in the number
        # of currently logged in user. Else, we send the new data for stats to the users
        if(replaced==False):
            data = json.dumps({'action':"newLogin"})
            for ws in connectedWS:
                ws.send(data)
        return jsonify(success=True,
                       message="Successfully signed in.",
                       data=response)


@app.route('/signup', methods=['POST'])
def sign_up():
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


@app.route('/logout', methods=['POST'])
def sign_out():
    print "Loggin out"
    token = request.form['token']
    email = database_helper.tokenToEmail(token)

    database_helper.signout(email)

    data = json.dumps({'action':"removeLogin"})
    for ws in connectedWS:
        ws.send(data)
    return jsonify(success=True,
                   message="Successfully signed out.")


@app.route('/changepassword', methods=['POST'])
def change_password():
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
            print "GET"
            numberOfVisits=database_helper.addVisit(email)
            print numberOfVisits
            token = database_helper.emailToToken(email)

            data = json.dumps({'visits': numberOfVisits,
                               'token':token,
                                'action':"newVisit"})

            for ws in connectedWS:
                ws.send(data)

            return jsonify(success=True,
                           message="User data retrieved.",
                           data=response)


@app.route('/postmessage', methods=['POST'])
def post_message():
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
    token = request.form['token']
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        response=database_helper.getmessagebytoken(token)
        if(response=="Error"):
            return jsonify(success=False,
                       message="No such user")
        else:
            return jsonify(success=True,
                           message="User messages received.",
                           data=response)

@app.route('/getusermessagebyemail', methods=['POST'])
def get_user_message_by_email():
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


@app.route('/getStats', methods=['POST'])
def getStats():
    token = request.form['token']
    active = database_helper.getNumberOfLoggedInUsers()

    numberOfVisits = database_helper.getNumberOfVisits(token)

    numberOfPosts = database_helper.getNumberOfPosts(token)


    return jsonify(success=True,
                active =active,
                visits=numberOfVisits,
                posts=numberOfPosts)


@app.route('/socket')
def socket():
    ws = None
    try:
        if request.environ.get('wsgi.websocket'):
            ws  = request.environ['wsgi.websocket']
            connectedWS.append(ws)
            while True:
                message = ws.receive()
                ws.send(ws)
        return
    except Exception, e:
        connectedWS.remove(ws)



if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    app.run(debug=True)