var getStats = function () {

    var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST","../getStats" , true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xmlhttp.onreadystatechange = function () {
            if(xmlhttp.readyState==4 && xmlhttp.status==200) {
                var stats = JSON.parse(xmlhttp.responseText);
                console.log(stats);

                active = stats.active;
                visits = stats.visits;
                averageVisits = Math.round(stats.averageVisits);
                posts = stats.posts;
                averagePosts = Math.round(stats.averagePosts);

                document.getElementById('stats_logged').innerHTML = active;
                document.getElementById('stats_visits').innerHTML = visits;
                document.getElementById('stats_posts').innerHTML = posts;

                document.getElementById('bar_average_visits_p').innerHTML=averageVisits;
                document.getElementById('bar_visits_p').innerHTML=visits;

                document.getElementById('bar_average_posts_p').innerHTML=averagePosts;
                document.getElementById('bar_posts_p').innerHTML=posts;

                var percentPost;
                var percentVisits;
                if(averagePosts > posts){
                    document.getElementById('bar_average_posts').style.height="100px";
                    percentPost = Math.round((posts/averagePosts)*100);
                    document.getElementById('bar_posts').style.height=percentPost+"px";

                }else{
                    document.getElementById('bar_posts').style.height="100px";
                    percentPost = Math.round((averagePosts/posts)*100);
                    document.getElementById('bar_average_posts').style.height=percentPost+"px";
                }

                if(averageVisits > visits){
                    document.getElementById('bar_average_visits').style.height="100px";
                    percentVisits = Math.round((visits/averageVisits)*100);
                    document.getElementById('bar_visits').style.height=percentVisits+"px";

                }else{
                    document.getElementById('bar_visits').style.height="100px";
                    percentVisits = Math.round((averageVisits/visits)*100);
                    document.getElementById('bar_average_visits').style.height=percentVisits+"px";
                }
            }
        };
        xmlhttp.send("token="+sessionStorage.token);


};

