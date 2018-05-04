var colors = ["red","blue","green","purple","orange","pink","black"];
var charts = {};
if($("#parameters").data('json_url')!=""){
    json_url = $("#parameters").data('json_url');
    console.log("Trying to retrieve "+json_url);

    $.getJSON("/"+$("#parameters").data('json_url'), function(json_data) {
        console.log(json_data);
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
    values = json["values"];
    indexes = json["file_labels"];
    indexes_array_loc = {};
    number_of_series = indexes.length
    series = [];
    var i=0;

    for(key in indexes){
        indexes_array_loc[indexes[key]]=key;
        series[i]={};
        series[i]["key"]=indexes[key];
        series[i]["values"]=[];
        series[i]["color"]=colors[i];

        i++;
    }
    for(var key in values){
      for(var j=0; j<values[key][metric].length; j++){
        series_label = values[key]["label"][j];
        loc = indexes_array_loc[series_label]
        series[loc]["values"].push({x:Number(key), y:values[key][metric][j]});
      }
    }
    add_chart(metric+"-graph", metric+" graph", series, "timestamp", metric);

    return series;
}

function add_chart(name, title, data, x_label, y_label){
  console.log("Adding chart "+name);

  nv.addGraph(function() {
    var chart = nv.models.lineWithFocusChart();

    chart.xAxis
        .tickFormat(d3.format(',f'));

    chart.yAxis
        .tickFormat(d3.format(',.2f'));

    chart.xAxis     //Chart x-axis settings
        .axisLabel(x_label)
        .tickFormat(d3.format(',r'));

    chart.yAxis     //Chart y-axis settings
        .axisLabel(y_label)
        .tickFormat(d3.format('.02f'));



    /* Done setting the chart up? Time to render it!*/
    var myData = data;

    d3.select("#"+name)    //Select the <svg> element you want to render the chart in.
        .datum(myData)     //Populate the <svg> element with chart data...
        .call(chart);          //Finally, render the chart!

    //Update the chart when window resizes.
    nv.utils.windowResize(function() { chart.update() });

    return chart;
  });
}
