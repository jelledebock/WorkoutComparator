var power_chart_area;
var charts = {};

json_data = JSON.parse(data);

colors = ["red","blue","green","purple","orange","pink","black"]
get_summary(json_data);
console.log(get_graph(json_data, 'power'));
console.log(get_graph(json_data, 'cadence'));

function get_graph(json, metric) {
    values = json["values"];
    indexes = json["file_labels"]
    indexes_array_loc = {};
    number_of_series = indexes.length
    console.log("Number of series : "+number_of_series);
    series = [];
    var i=0;

    for(key in indexes){
        indexes_array_loc[indexes[key]]=key;
        series[i]={};
        series[i]["label"]=indexes[key];
        series[i]["data"]=[];
        series[i]["borderColor"]=colors[i];
        series[i]["showLine"]=true;
        series[i]["fill"]=false;
        series[i]["pointRadius"]=0;

        i++;
    }
    console.log(indexes_array_loc);
    for(var key in values){
      for(var j=0; j<values[key][metric].length; j++){
        series_label = values[key]["label"][j];
        loc = indexes_array_loc[series_label]
        series[loc]["data"].push({x:Number(key), y:values[key][metric][j]});
      }
    }
    power_chart_area = document.getElementById(metric+"-graph").getContext('2d');
    make_chart(power_chart_area, series, metric);

    return series;
}
function get_summary(json){
  summary=json_data["summary"];
  summary_html = '<table class="table"><thead class="thead-dark"><tr>'+
                    '<th>File</th>'+
                    '<th>Normalized power</th>'+
                    '<th>AVG power</th>'+
                    '<th>AVG heart rate</th>'+
                    '<th>AVG cadence</th>'+
                    '<th>Max power</th>'+
                    '<th>Max cadence</th>'+
                    '<th>Max heart rate</th>'+
                    '</tr></thead><tbody>';

    for(var key in summary){
      summary_html += '<tr>';
      summary_html += '<td>'+key+'</td>';
      summary_html += '<td>'+summary[key]['NP']+'</td>';
      summary_html += '<td>'+summary[key]['avg_power']+'</td>';
      summary_html += '<td>'+summary[key]['avg_heart_rate']+'</td>';
      summary_html += '<td>'+summary[key]['avg_cadence']+'</td>';
      summary_html += '<td>'+summary[key]['max_power']+'</td>';
      summary_html += '<td>'+summary[key]['max_cadence']+'</td>';
      summary_html += '<td>'+summary[key]['max_heart_rate']+'</td>';
      summary_html += '</tr>';
    }

    summary_html += '</tbody></table>';
    console.log(summary_html);
    $("#summary-stats").html(summary_html);
}
function reset_power_zoom(){
  charts["power"].resetZoom();
}

function reset_cadence_zoom() {
  charts["cadence"].resetZoom();
}
function make_chart(chart_area, data, metric){
    charts[metric] = new Chart(chart_area, {
      type: 'scatter',
      data: {
          datasets: data
      },
      options: {
                    title: {
                        display: true,
                        text: metric
                    },
                    scales: {
                      xAxes: [{
                          type: 'linear',
                          position: 'bottom'
                      }],
                     yAxes: [{
                         ticks: {
                            beginAtZero: false,
                            stepSize: 100,
                            maxTicksLimit: 10
                        }
                     }]
                    },
                    // Container for pan options
                    pan: {
                      // Boolean to enable panning
                      enabled: true,

                      // Panning directions. Remove the appropriate direction to disable
                      // Eg. 'y' would only allow panning in the y direction
                      mode: 'x',
                      rangeMin: {
                      // Format of min pan range depends on scale type
                      x: null,
                      y: null
                      },
                      rangeMax: {
                      // Format of max pan range depends on scale type
                      x: null,
                      y: null
                      }
                    },
                    // Container for zoom options
                    zoom: {
                      // Boolean to enable zooming
                      enabled: true,

                      // Enable drag-to-zoom behavior
                      drag: true,

                      enabled: true,
          						mode: 'x',
          						sensitivity: 3,
          						limits: {
          							max: 10,
          							min: 0.5
          						}
                    }
                  }
      });
}
