const url = "http://127.0.0.1:8000/"


const DATAplatform = 'Plateform'
const DATAy = 'y'

// viz sex_survived
Highcharts.getJSON(url + "sex_survived",
  function (data) {
    const platform = data.map(d => [d.name,  d.pourcent]);

    Highcharts.chart('my_first_graph', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
      },

      
      title: {
        text: 'Représentation des survivants en fonction du genre'
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      accessibility: {
        point: {
          valueSuffix: '%'
        }
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Pourcentage',
        colorByPoint: true,
        data: platform
      }]
    })
  }
);

// viz pclass survived

Highcharts.getJSON(url + "pclass_survived",
  function (data) {
    const platform = data.map(d => [d.name,  d.pourcent]);

    Highcharts.chart('my_second_graph', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
      },
      title: {
        text: 'Représentation des survivants en fonction du type de ticket'
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      accessibility: {
        point: {
          valueSuffix: '%'
        }
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Pourcentage',
        colorByPoint: true,
        data: platform
      }]
    })
  }
);

// viz survived by age
Highcharts.getJSON(url + "age_survived",
  function (data)
  {
    const type = data.map(d => [d.name,  d.pourcent]); // nom des colonnes sur json
    Highcharts.chart('my_third_graph',
    {
      chart: {
        type: 'column'
      },
      title: {
        text: 'Représentation des survivants en fonction de la classe d\'âge'
      },
      accessibility: {
        announceNewData: {
          enabled: true
        }
      },
      xAxis: {
        type: 'category'
      },
      yAxis: {
        title: {
          text: 'Nombre de survivants par classe d\'âge'
        }
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        series: {
          borderWidth: 0,
          dataLabels: {
            enabled: true,
            format: '{point.y}'
          }
        }
      },

      tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
      },

      series: [
        {
          name: "",
          colorByPoint: true,
          data: type
        }
      ]
    })
  }
);

// viz selon les prédictions
Highcharts.getJSON(url + "count_predictions",
  function (data) {
    const platform = data.map(d => [d.name,  d.pourcent]);

    Highcharts.chart('my_fourth_graph', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: False,
        type: 'pie'
      },
      title: {
        text: 'Plateformes présentes dans les prochaine sortie'
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      accessibility: {
        point: {
          valueSuffix: '%'
        }
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Console',
        colorByPoint: true,
        data: platform
      }]
    })
  }
);


// example 
Highcharts.getJSON(url + "age_survived",
  function (data)
  {
    const pblsh = data.map(d => [d.pourcent]);
    const nme = data.map(d => [d.name]);
    Highcharts.chart('my_fifth_graph', {
      chart: {
        type: 'bar'
      },
      title: {
        text: ''
      },

      xAxis: {
        categories: nme,
        title: {
          text: null
        }
      },
      yAxis: {
        min: 0,
        title: {
          text: 'Nombre de jeux ',
          align: 'high'
        },
        labels: {
          overflow: 'justify'
        }
      },
      tooltip: {
        valueSuffix: ' jeux'
      },
      plotOptions: {
        bar: {
          dataLabels: {
            enabled: false
          }
        }
      },
      legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 80,
        floating: true,
        borderWidth: 1,
        backgroundColor:
          Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
        shadow: true
      },
      credits: {
        enabled: false
      },
      series: [{

        name: 'A venir',
        data: pblsh
      }]
    })
  }
)
