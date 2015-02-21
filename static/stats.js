
var initChart = function (barData) {
    console.log(barData);

    var vis = d3.select('#visualisation'),
    WIDTH = 500,
    HEIGHT = 200,
    MARGINS = {
      top: 20,
      right: 20,
      bottom: 20,
      left: 50
    },
    xRange = d3.scale.ordinal().rangeRoundBands([MARGINS.left, WIDTH - MARGINS.right], 0.1).domain(barData.map(function (d) {
      return d.x;
    })),


    yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,
      d3.max(barData, function (d) {
        return d.y;
      })
    ]),

    xAxis = d3.svg.axis()
      .scale(xRange)
      .tickSize(5)
      .tickSubdivide(true),

    yAxis = d3.svg.axis()
      .scale(yRange)
      .tickSize(5)
      .orient("left")
      .tickSubdivide(true);


    vis.append('svg:g')
    .attr('class', 'x axis')
    .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
    .call(xAxis);

    vis.append('svg:g')
    .attr('class', 'y axis')
    .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
    .call(yAxis);

    vis.selectAll('rect')
    .data(barData)
    .enter()
    .append('rect')
    .attr('x', function (d) {
      return xRange(d.x);
    })
    .attr('y', function (d) {
      return yRange(d.y);
    })
    .attr('width', xRange.rangeBand())
    .attr('height', function (d) {
      return ((HEIGHT - MARGINS.bottom) - yRange(d.y));
    })
    .attr('fill', 'grey');

};


function getDataForGraph(){
    email = JSON.parse(sessionStorage.loggedInUser).email;
    console.log(JSON.parse(sessionStorage.loggedInUser).email);


    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","../getVisitors" , true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState==4 && xmlhttp.status==200) {

            var visitors = JSON.parse(xmlhttp.responseText);
            data = visitors.data[0];

            var barData = [{
                'x': 1,
                'y': data[1]
                }, {
                'x': 2,
                'y': data[2]
                }, {
                'x': 3,
                'y': data[3]
                }, {
                'x': 4,
                'y': data[4]
                }, {
                'x': 5,
                'y': data[5]
                }, {
                'x': 6,
                'y': data[6]
                }, {
                'x': 7,
                'y': data[7]
                }, {
                'x': 8,
                'y': data[8]
                }, {
                'x': 9,
                'y': data[9]
                }, {
                'x': 10,
                'y': data[10]
                }, {
                'x': 11,
                'y': data[11]
                }, {
                'x': 12,
                'y': data[12]
                }];
            initChart(barData);
        }
    };
    xmlhttp.send("email="+email);


}

