var colors = ["red","blue","green","purple","orange","pink","black"];
var charts = {};
var json_url;

if($("#parameters").data('json_url')!=""){
    json_url = $("#parameters").data('json_url');
    console.log("Trying to retrieve "+json_url);

    $.getJSON('/'+$("#parameters").data('json_url'), function(json_data) {
        get_summary(json_data);
        console.log(json_data);
        console.log(get_graph(json_data, 'power'));
        console.log(get_graph(json_data, 'cadence'));
    });}
else{
    json_data = JSON.parse(data);
    get_summary(json_data);
    console.log(json_data);
    console.log(get_graph(json_data, 'power'));
    console.log(get_graph(json_data, 'cadence'));
}

function get_graph(json, metric) {
    series = [];
    indexes = json["file_labels"];

    for(key in indexes) {
        file_label = json['file_labels'][key];
        series[key]={};
        series[key].key=file_label;
        series[key].values=[];
        series[key].color=colors[key];

          $.ajax({
             async: false,
             url: '/values?metric='+metric+'&json_url='+encodeURIComponent(json_url)+'&file_label='+file_label,
             dataType: "json",
             success: function(data){
                series[key].values=data;
                console.log("Done retrieving data of key "+key);
             }
          });
    }
    add_chart(metric+"-graph", metric+" graph", series, "timestamp", metric);

    return series;
}

function add_chart(name, title, data, x_label, y_label){
  console.log("Adding chart "+name);

  nv.addGraph(function() {
    var chart = nv.models.lineWithFocusChart();

    chart.y2Axis
          .tickFormat(d3.format(',.2f'));

    chart.xAxis     //Chart x-axis settings
        .axisLabel(x_label)
        .tickFormat(d3.format(',r'));

    chart.yAxis     //Chart y-axis settings
        .axisLabel(y_label)
.tickFormat(d3.format('.02f'));


    /* Done setting the chart up? Time to render it!*/
    d3.select("#"+name)    //Select the <svg> element you want to render the chart in.
        .datum(data)     //Populate the <svg> element with chart data...
        .call(chart);          //Finally, render the chart!

    //Update the chart when window resizes.
    nv.utils.windowResize(function() { chart.update() });

    return chart;
  });
}
