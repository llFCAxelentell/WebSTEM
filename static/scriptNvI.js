google.charts.load('current', {
    'packages': ['corechart']
});
google.charts.setOnLoadCallback(drawVisualization);

function drawVisualization() {
    // Some raw data (not necessarily accurate)
    var data = google.visualization.arrayToDataTable([
          ['Nivel', 'Compuestos','Elementos', 'Clientes', 'Dinero'],
          ['1', 165, 938, 998, 450],
          ['2', 135, 1120, 1268, 288],
          ['3', 157, 1167, 807, 397],
          ['4', 139, 1110, 968, 215],
          ['5', 136, 691, 1026, 366]
        ]);

    var options = {
        title: 'Promedio de indicadores por nivel',
        vAxis: {
            title: 'Indicadores'
        },
        hAxis: {
            title: 'Nivel'
        },
        seriesType: 'bars',
    
    };

    var chart = new google.visualization.ComboChart(document.getElementById('chart_divNvI'));
    chart.draw(data, options);
}
