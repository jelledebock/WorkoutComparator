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
