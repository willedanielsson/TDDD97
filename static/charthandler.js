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


                var percentPost;
                var percentVisits;

                console.log("Redraws the canvas");
                drawVisits(visits, averageVisits);
                drawPosts(posts, averagePosts);
                /*
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
                */
            }
        };
        xmlhttp.send("token="+sessionStorage.token);


};

google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(drawChart);

function drawChart(){

}

function drawVisits (your, average){
    var data = new google.visualization.DataTable;
    data.addColumn('string', 'Visitors');
        data.addColumn('number', 'Visits');
        data.addRows([
          ['Your', your],
          ['Average', average]
        ]);

        // Set chart options
        var options = {'title':'Number of visits',
                       'width':400,
                       'height':300};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.BarChart(document.getElementById('visit_chart_div'));
        chart.draw(data, options);
}

function drawPosts (your, average){
    var data = new google.visualization.DataTable;
    data.addColumn('string', 'Posts');
        data.addColumn('number', 'Posts');
        data.addRows([
          ['Your', your],
          ['Average', average]
        ]);

        // Set chart options
        var options = {'title':'Number of posts',
                       'width':400,
                       'height':300};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.BarChart(document.getElementById('post_chart_div'));
        chart.draw(data, options);
}