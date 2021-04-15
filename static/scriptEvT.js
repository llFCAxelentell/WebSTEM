google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Edad', 'Tiempo jugado'],
          [ 10,      50],
          [ 17,      20],
          [ 16,     120],
          [ 9,      30],
          [ 15,      15],
          [ 12,    32]
        ]);

        var options = {
          title: 'Edad vs Tiempo jugado',
          hAxis: {title: 'Edad (años)'},
          vAxis: {title: 'Tiempo jugado (min)'},
          legend: 'none'
        };

        var chart = new google.visualization.ScatterChart(document.getElementById('chart_divEvT'));

        chart.draw(data, options);
      }
