loadCharts()
function loadCharts() {
  console.log('Setting up charts')
  if (pre_graph_data != null && pre_graph_data.portfolios.length > 0) {
    let data = pre_graph_data
    let labels = []
    for (var i = 0; i < data.portfolios[0].length; i++) {
      labels.push(i)
    }
    let datasets = []
    for (var i = 0; i < data.portfolios.length; i++) {
      temp = {
        data: data.portfolios[i],
        borderColor: getRandomColor(),
        borderWidth: 1,
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 0,
      }
      datasets.push(temp)
    }
    setupPreChart0(labels, datasets)
  }
}

function setupPreChart0(labels, datasets) {
  var ctx = document.getElementById("pre-chart0").getContext('2d');
  var preChart0 = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: datasets,
      },
      options: {
          legend: {
            display: false,
          },
          responsive: false,
          title: {
            display: true,
            text: 'Monte Carlo Simulation Results',
          },
          scales: {
            xAxes: [{
              ticks: {
                maxTicksLimit: 10,
              }
            }]
          },
          elements: {
            line: {
              tension: 0,
            }
          },
          animation: {
            duration: 0,
          },
          hover: {
            animationDuration: 0,
          },
          responsiveAnimationDuration: 0,
          tooltips: {
            enabled: false
          },
      }
  });
}

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
