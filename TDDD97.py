from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
app = Flask(__name__)

import database_helper


@app.route('/')
def hello_world():
    database_helper.init()
    return render_template('client.html')

@app.route('/signin', methods=['GET'])
def sign_in():
    print "Signin in"
    email = request.args.get('email')
    password = request.args.get('password')
    response = database_helper.signin(email, password)
    if response=="Error":
        return jsonify(success=False,
                       message="Wrong username or password.",)
    else:
        return jsonify(success=True,
                       message="Successfully signed in.",
                       data=response)


@app.route('/signup', methods=['GET'])
def sign_up():
    print "Signin up"
    email = request.args.get('email')
    password = request.args.get('password')
    firstname = request.args.get('firstname')
    familyname = request.args.get('familyname')
    gender = request.args.get('gender')
    city = request.args.get('city')
    country = request.args.get('country')
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

@app.route('/changepassword', methods=['GET'])
def change_password():
    print "Changing pass"
    token = request.args.get('token')
    oldpass = request.args.get('oldpass')
    newpass = request.args.get('newpass')
    response = database_helper.changepassword(token, oldpass, newpass)
    if(response=="Success"):
        return jsonify(success=True,
                       message="Password changed.")
    elif(response=="NotLoggedIn"):
        return jsonify(success=False,
                       message="You are not logged in.")
    else:
        return jsonify(success=False,
                       message="Error")


@app.route('/getuserdatabytoken', methods=['GET'])
def get_user_data_by_token():
    print "Getting data for user"
    token = request.args.get('token')
    response = database_helper.getuserdatabytoken(token)
    if response=="Error":
        return jsonify(success=False,
                       message="No such user.")
    else:
        return jsonify(success=True,
                       message="User data retrieved.",
                       #data=response[0]+", "+response[1]+", "+response[2]+", "+response[3]+", "+response[4]+", "+response[5])
                        data=response)
@app.route('/getuserdatabyemail', methods=['GET'])
def get_user_data_by_email():
    print "Getting data for friend"
    token = request.args.get('token')
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        email = request.args.get('email')
        response = database_helper.getuserdatabyemail(email)
        if(response=="Error"):
            return jsonify(success=False,
                           message="No such user.")
        else:
             return jsonify(success=True,
                           message="User data retrieved.",
                           data=response[0]+", "+response[1]+", "+response[2]+", "+response[3]+", "+response[4]+", "+response[5])

@app.route('/postmessage', methods=['GET'])
def post_message():
    print "Posting message"
    token = request.args.get('token')
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        email = request.args.get('email')
        userExist = database_helper.getuserdatabyemail(email)
        if(userExist=="Error"):
            return jsonify(success=False,
                           message="No such user.")
        else:
            message = request.args.get('message')
            response = database_helper.postmessage(email, message)
            if(response == "Success"):
                return jsonify(success=True, message="Message posted.")
            else:
                return jsonify(success=False, message="Failed to post.")

@app.route('/getusermessagebytoken', methods=['GET'])
def get_user_message_by_token():
    print "Getting message by token"
    token = request.args.get('token')
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

@app.route('/getusermessagebyemail', methods=['GET'])
def get_user_message_by_email():
    print "Getting message by email"
    token = request.args.get('token')
    loggedIn = database_helper.getuserdatabytoken(token)
    if(loggedIn=="Error"):
        return jsonify(success=False,
                       message="Not logged in.")
    else:
        email = request.args.get('email')
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