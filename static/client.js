// Variables
var messages;
var userInfo;



var ws = new WebSocket("ws://127.0.0.1:5000/socket");

ws.onopen = function () {

}

ws.onmessage = function (msg) {
    console.log("Message är:");
    console.log(msg.data);
    if(msg.data==sessionStorage.token){
        closeSession();
    }
}


window.onload = function(){
 	displayView();

}
/*
Function that removes the current session and brings the user back to welcome view
 */
var closeSession = function(){
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("loggedInUser");
    location.reload();

}
/*
Function that registers a new user
Input = Email, password, name, gender, city and country
Returns:
    Sucess: json with a success-message
    False : json with error message
 */
var register = function(){
	// Check if passwords match
	if(document.getElementById("reg_pass").value !== document.getElementById("reg_re_pass").value){
		document.getElementById("register_warning").innerHTML="Passwords didn't match";

	}else{
		//password match
        var email = document.getElementById("reg_email").value;
        var password = document.getElementById("reg_pass").value;
        var firstname = document.getElementById("first_name").value;
        var familyname = document.getElementById("last_name").value;
        var gender = document.getElementById("gender").value;
        var city = document.getElementById("city").value;
        var country = document.getElementById("country").value;

        if(email!="" && password !="" && firstname!="" && familyname!="" &&
        gender!="" && city!="" && country!="") {

            xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "../signup", true);
            xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            xmlhttp.onreadystatechange = function () {
                if(xmlhttp.readyState==4 && xmlhttp.status==200) {

                    var response = JSON.parse(xmlhttp.responseText);
                    console.log(response);
                    if(response.success==true){
                        document.getElementById('register_warning').innerHTML="You have been registered!";
                    }else{
                        document.getElementById('register_warning').innerHTML=response.message;
                    }

                }else if(xmlhttp.status!=200){
                    document.getElementById('register_warning').innerHTML="Registration Failed!";
                }
            };
            xmlhttp.send("email="+email+"&password="+password+"&firstname="+firstname+"&familyname="+familyname+
            "&gender="+gender+"&city="+city+"&country="+country);

        }else{
            // NOt all values were filled
            document.getElementById('register_warning').innerHTML="Fill all the fields!";
        }
	}

}

/*
Function that try to login the user.
Input = Email and password
Returns:
    Sucess: json with a random token which we add to sessionStorage
    False : json with error message
 */
var login = function(){
	var email = document.getElementById("log_email").value;
    var password = document.getElementById("log_pass").value;

    if(email!="" && password!="") {

        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "../signin", true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xmlhttp.onreadystatechange = function () {
            if(xmlhttp.readyState==4 && xmlhttp.status==200) {

                var response = JSON.parse(xmlhttp.responseText);
                console.log(response.data);
                sessionStorage.token = response.data;
                displayView();

            }else if(xmlhttp.status!=200){
                document.getElementById('failed_login').innerHTML="Login Failed!";
            }
        };

    }else{
        // Email or password was not set
        document.getElementById('failed_login').innerHTML="Login Failed!";
    }
        xmlhttp.send("email="+email+"&password="+password);
    
        location.reload();

}

/*
Function that sends the message to the database
Input = Target: decides if it is on a friends wall or not (gets the token from sessionStorage and email from session)
Returns:
    Success: A success-message
    Error : A error-message
 */
postText = function(target){
    var text;
    if(target=="friend"){

        text = document.getElementById('friend_post_textarea').value;
    }else{
        text = document.getElementById('post_textarea').value;
    }

    if(text!=""){
        var email;
        if(target=="friend"){
            email = document.getElementById('friend_email').innerHTML;
        }else{
            email = JSON.parse(sessionStorage.getItem("loggedInUser")).email;
        }

        if(email!=""){
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST","../postmessage" , true);
            xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            xmlhttp.onreadystatechange = function () {
                if(xmlhttp.readyState==4 && xmlhttp.status==200) {

                    var response = JSON.parse(xmlhttp.responseText);
                    console.log(response);

                }
            };
            xmlhttp.send("token="+sessionStorage.token+"&message="+text+"&email="+email);
        }
    }
}

friendPostText = function(){
	var text = document.getElementById('friend_area').value;
	serverstub.postMessage(sessionStorage.token, text, document.getElementById('friend_email').innerHTML);
}

/*
Function retrieves data for the logged in user
Input = None (gets the token from sessionStorage)
Returns:
    Sucess: None (Fills the user-info with data)
    False : Nothing
 */
getHomeData = function(){
    if(sessionStorage.token!=="undefined"){
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST","../getuserdatabytoken" , true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xmlhttp.onreadystatechange = function () {
            if(xmlhttp.readyState==4 && xmlhttp.status==200) {

                var userInfo = JSON.parse(xmlhttp.responseText);

                document.getElementById('user_email').innerHTML = userInfo.data[0];
                document.getElementById('user_name').innerHTML = userInfo.data[1] + " " + userInfo.data[2];
                document.getElementById('user_location').innerHTML = userInfo.data[4] +", " + userInfo.data[5];

                var data= {
                    "email":userInfo.data[0],
                    "firstName": userInfo.data[1],
                    "lastName": userInfo.data[2],
                    "gender": userInfo.data[3],
                    "city": userInfo.data[4],
                    "country": userInfo.data[5]
                };


                user = JSON.stringify(data);
                sessionStorage.setItem("loggedInUser",user);

            }
        };
        xmlhttp.send("token="+sessionStorage.token);

        // Get the messages
        getUserMessages();
    }
}
/*
Function retrieves messages for the logged in user
Input = None (gets the token from sessionStorage)
Returns:
    Sucess: None (Fills the message-wall with data)
    False : Nothing
 */
var getUserMessages = function(){
    token = sessionStorage.token;
    if(token!=="undefined") {

        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", "../getusermessagebytoken", true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

                var messages = JSON.parse(xmlhttp.responseText);
                document.getElementById('post_list_list').innerHTML = '';
                for (var i = messages.data.length - 1; i >= 0; i--) {
                    var listItem = document.createElement("li");
                    listItem.innerHTML = messages.data[i][0];
                    document.getElementById('post_list_list').appendChild(listItem);
                }

            }
        };
        xmlhttp.send("token=" + token);
    }
}

/*
Function changes password of user
Input = token from sessions, oldpass, newpass and repeated newpass is sent in by form
Returns:
    Sucess: Success-message
    False: Error-message
 */
newPass = function(){
    var oldPass = document.getElementById('old_pass').value;
    var newPass = document.getElementById('new_pass').value;
    var reNewPass = document.getElementById('re_new_pass').value;

	if(oldPass!=="" && newPass!=="" && reNewPass!==""){

		if(newPass==reNewPass){
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "../changepassword", true);
            xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

                    var response = JSON.parse(xmlhttp.responseText);

                    if(response.success==true){
                        document.getElementById('new_pass_text').innerHTML="Password changed";
                    }else{
                        document.getElementById('new_pass_text').innerHTML=response.message;
                    }
                }
            };

            xmlhttp.send("token="+sessionStorage.token+"&oldpass="+oldPass+"&newpass="+newPass);

            //serverstub.changePassword(sessionStorage.token, oldPass, newPass);

		}else{
			document.getElementById('new_pass_text').innerHTML="Password's didnt match";

		}
	}else{

	}

}

logout = function(){


    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","../logout" , true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState==4 && xmlhttp.status==200) {

            var response = JSON.parse(xmlhttp.responseText);

        }
    };
    xmlhttp.send("token="+sessionStorage.token);
    closeSession();
}
/*
Function retrieves messages for the logged in user
Input = Token from sessions, text from input and email from session
Returns:
    Sucess: None (Fills the info with data)
    False : Error message
 */
findUser = function(){
    var searchedUser = document.getElementById('searched_friend').value;

    if(searchedUser!==""){
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST","../getuserdatabyemail" , true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xmlhttp.onreadystatechange = function () {
            if(xmlhttp.readyState==4 && xmlhttp.status==200) {

                var friendInfo = JSON.parse(xmlhttp.responseText);

                if(friendInfo.success==true){
                    document.getElementById('user_search_text').innerHTML="";
                    console.log(friendInfo);
                    document.getElementById('friend_email').innerHTML = friendInfo.data[0];
		            document.getElementById('friend_name').innerHTML = friendInfo.data[1]+" "+friendInfo.data[2];
		            document.getElementById('friend_location').innerHTML = friendInfo.data[4]+", "+friendInfo.data[5];

                    // Retrieves messages for the friend
                    getFriendMessages(friendInfo.data[0]);
                }else{
                    // No user with that name
                    document.getElementById('user_search_text').innerHTML="Couldn't find a user";
                }

            }
        };
        xmlhttp.send("token="+sessionStorage.token+"&email="+searchedUser);

    }
}

/*
Function retrieves messages for the searched user
Input = Token from sessions and a specified email
Returns:
    Sucess: None (Fills the wall with data)
    False : Error message
 */
var getFriendMessages = function(email){
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST","../getusermessagebyemail" , true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xmlhttp.onreadystatechange = function () {
            if(xmlhttp.readyState==4 && xmlhttp.status==200) {

                var friendMessages = JSON.parse(xmlhttp.responseText);
                document.getElementById('friend_post_list_list').innerHTML = '';
                if(friendMessages.success==true){
                    document.getElementById('user_search_text').innerHTML="";

                    for(var i=friendMessages.data.length-1; i>=0; i--){
                        var listItem = document.createElement("li");
                        listItem.innerHTML = friendMessages.data[i][0];
                        document.getElementById('friend_post_list_list').appendChild(listItem);
                    }
                }else{
                    document.getElementById('user_search_text').innerHTML=friendMessages.message;
                }

            }
        };
        xmlhttp.send("token="+sessionStorage.token+"&email="+email);

}
/*
Function that reloads the messages
Input: None (try to get the data from the HTML
Later calls getFriendMessages if email was set
 */
reloadFriendMessage = function(){
	email = document.getElementById('friend_email').innerHTML;
    if(email!=""){
        getFriendMessages(email);
    }

}

/*
Function that determines what view to show
Input = None (gets the token from sessionStorage)
Returns:
    If user is logged in (token is set), show the profile
    If not, back to welcome-screen
 */
displayView = function(){
    console.log(sessionStorage.token);
	if(sessionStorage.token==undefined){
        console.log("Går in");
		document.getElementById('welcome_content').innerHTML = document.getElementById('welcome_view').innerHTML;
	}else{
		document.getElementById('welcome_content').innerHTML = document.getElementById('profile_view').innerHTML;

		// Shows the data for the home view which is shown by default
		getHomeData();
	}
}

/*
Function that determines what tab to shoq
Input = A string that is home, browse or account
Returns:
    None (shows the correct tab)
 */

clickedNav = function(link){

	if(link==="home"){
		document.getElementById('home_content').style.display= "block";
		document.getElementById('browse_content').style.display= "none";
		document.getElementById('account_content').style.display= "none";
	}else if(link==="browse"){
		document.getElementById('home_content').style.display= "none";
		document.getElementById('browse_content').style.display= "block";
		document.getElementById('account_content').style.display= "none";
	}else if(link==="account"){
		document.getElementById('home_content').style.display= "none";
		document.getElementById('browse_content').style.display= "none";
		document.getElementById('account_content').style.display= "block";
	}

}
