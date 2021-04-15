google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Tiempo', 'Compuestos'],
          [ 10,      2],
          [ 17,      7],
          [ 25,     12],
          [ 70,      55],
          [ 73,      57],
          [ 100,    72]
        ]);

        var options = {
          title: 'Tiempo jugado vs Compuestos hechos',
          hAxis: {title: 'Tiempo (min)'},
          vAxis: {title: 'Compuestos (unidades)'},
          legend: 'none'
        };

        var chart = new google.visualization.ScatterChart(document.getElementById('chart_divTvC'));

        chart.draw(data, options);
      }
