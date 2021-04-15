google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Compuestos', 'Elementos'],
          [ 10,      13],
          [ 5,      10],
          [ 7,     19],
          [ 2,      10],
          [ 7,      12],
          [ 9,    21]
        ]);

        var options = {
          title: 'Compuestos vendidos vs Elementos comprados',
          hAxis: {title: 'Comuestos vendidos'},
          vAxis: {title: 'Elementos comprados'},
          legend: 'none'
        };

        var chart = new google.visualization.ScatterChart(document.getElementById('chart_divCvE'));

        chart.draw(data, options);
      }