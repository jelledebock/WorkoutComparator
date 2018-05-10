function get_summary(json_data){
  summary=json_data["summary"];
  summary_html = '<table class="table"><thead class="thead-dark"><tr>'+
                    '<th>File</th>'+
                    '<th>NP</th>'+
                    '<th>AVG power</th>'+
                    '<th>AVG BPM</th>'+
                    '<th>AVG cadence</th>'+
                    '<th>Max power</th>'+
                    '<th>Max cadence</th>'+
                    '<th>Max BPM</th>'+
                    '<th>Edit</th>'+
                    '</tr></thead><tbody>';

    for(var key in summary){
      summary_html += '<tr>';
      summary_html += '<td>'+key+'</td>';
      summary_html += '<td>'+Math.round(summary[key]['NP'])+'</td>';
      summary_html += '<td>'+summary[key]['avg_power']+'</td>';
      summary_html += '<td>'+summary[key]['avg_heart_rate']+'</td>';
      summary_html += '<td>'+summary[key]['avg_cadence']+'</td>';
      summary_html += '<td>'+summary[key]['max_power']+'</td>';
      summary_html += '<td>'+summary[key]['max_cadence']+'</td>';
      summary_html += '<td>'+summary[key]['max_heart_rate']+'</td>';
      summary_html += '<td><b>Time offset: </b><input type="number" name="time-offset" ' ;
      summary_html += 'value="0"><input type="submit" id="edit_time" data-file_key="'+key+'" value="edit"></td>';
      summary_html += '</tr>';
    }

    summary_html += '</tbody></table>';
    $("#summary-stats").html(summary_html);
}

$(document).change(function() {
  $('input#edit_time').on('click', function() {
    var key = $(this).data('file_key');
    var value = $(this).prev('input').val();
    $.ajax({
      url: "/edit?file_name="+encodeURIComponent(json_url)+"&file_subcomponent="+encodeURIComponent(key)+'&offset='+encodeURIComponent(value),
      data: '',
      success: function () {
         window.location.reload(true);
      },
      dataType: 'json'
    });
  });
});


