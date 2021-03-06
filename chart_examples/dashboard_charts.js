google.setOnLoadCallback(drawVisualization);

function httpGet_to_array(theUrl)
{
    var xmlHttp = null;

    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    var array = JSON.parse( xmlHttp.responseText );
    var data = [];
    cols = Object.keys(array['data'][0]);
    data.push(cols)
    for(var i = 0; i < array['data'].length; i++ ){
      var row = [];
      for(var j = 0; k=j < cols.length; j++){
        row.push(array['data'][i][cols[j]]);
      }
      data.push(row)
    }
    return data;
}

function drawVisualization() {

  var data = new google.visualization.arrayToDataTable(httpGet_to_array("http://127.0.0.1:5000/data/top-countries"));

  var regionTable = new google.visualization.ChartWrapper({
      "containerId": 'region_table',
      "chartType": 'Table',
      "refreshInterval": 1000,
      "dataTable": data,
      "options": {
        "showRowNumber" : true,
        "width": 630,
        "height": 440,
        "is3D": false,
        "title": "Sessions by Day"
     }
    });

    regionTable.draw();

    var options = {
        "width": 630,
        "height": 440,
        "title": "Visitors by Region"
      };

    var regionChart = new google.visualization.GeoChart(document.getElementById('regions_map'));

    regionChart.draw(data, options);

}
