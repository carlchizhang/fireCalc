loadCharts()
function loadCharts() {
  console.log('Setting up charts')
  //pre-retirement charts
  if (pre_graph_data != null && pre_graph_data.portfolios.length > 0) {
    let data = pre_graph_data
    let labels = []
    let targetLine = []
    for (var i = 0; i < data.portfolios[0].length; i++) {
      if (i % 5 == 0) {
        labels.push('Year ' + i)
      }
      else {
        labels.push('')
      }
      targetLine.push(pre_graph_data.stats.target)
    }
    let datasets = []
    datasets.push({
      label: 'Target Amount',
      data: targetLine,
      borderColor: '#E60000',
      borderWidth: 4,
      fill: false,
      borderDash: [15, 5],
      pointRadius: 0,
      pointHoverRadius: 0,
      pointHitRadius: 0,
    })
    for (var i = 0; i < data.portfolios.length; i++) {
      temp = {
        label: null,
        data: data.portfolios[i],
        borderColor: getRandomColor(),
        borderWidth: 1,
        fill: false,
        pointRadius: 1,
        pointHoverRadius: 2,
        pointHitRadius: 12,
      }
      datasets.push(temp)
    }
    setupPreChart0(labels, datasets, data.stats)
    setupPreChart1(data.histogram.bins, data.histogram.years, data.stats)
  }

  //post-returement charts
  //console.log(post_graph_data)
  if (post_graph_data != null && post_graph_data.portfolios.length > 0) {
    let data = post_graph_data
    let labels = []
    let initialVal = data.portfolios[0][0]
    let initialLine = []
    for (var i = 0; i < data.portfolios[0].length; i++) {
      if (i % 5 == 0) {
        labels.push('Year ' + i)
      }
      else {
        labels.push('')
      }
      initialLine.push(initialVal)
    }
    let datasets = []
    datasets.push({
      label: 'Starting Amount',
      data: initialLine,
      borderColor: '#E60000',
      borderWidth: 4,
      fill: false,
      borderDash: [15, 5],
      pointRadius: 0,
      pointHoverRadius: 0,
      pointHitRadius: 0,
    })
    for (var i = 0; i < data.portfolios.length; i++) {
      temp = {
        label: null,
        data: data.portfolios[i],
        borderColor: getRandomColor(),
        borderWidth: 1,
        fill: false,
        pointRadius: 1,
        pointHoverRadius: 2,
        pointHitRadius: 12,
      }
      datasets.push(temp)
    }
    setupPostChart0(labels, datasets, data.stats)

    success_rates = []
    for (var i = 0; i < data.stats.failure_rates.length; i++) {
      success_rates.push(100 - data.stats.failure_rates[i])
    }
    //console.log(success_rates)
    setupPostChart1(data.histogram.bins, data.histogram.years, success_rates)
  }
}

function setupPreChart0(labels, datasets, stats) {
  var ctx = document.getElementById("pre-chart0").getContext('2d');
  var preChart0 = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: datasets,
      },
      options: {
          legend: {
            display: true,
            labels: {
              filter: function(item, chart) {
                //console.log(item)
                if (item.text == null) {
                  return null
                }
                else {
                  return item.text
                }
              },
            },
          },
          scales: {
            xAxes: [{
              ticks: {
                //maxTicksLimit: Math.round(labels.length / 5),
              }
            }],
            yAxes: [{
              type: 'linear',
              ticks: {
                // Include a dollar sign in the ticks
                callback: function(value, index, values) {
                  if (value >= 1000000) {
                    return '$' + Math.round(value/10000)/100 + 'M'
                  }
                  return '$' + value
                },
              },
            }],
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
            callbacks: {
              title: function(tooltipItem, data) {
                //console.log(tooltipItem)
                return 'Year ' + tooltipItem[0].index
              },
              label: function(tooltipItem, data) {
                //console.log(tooltipItem)
                //console.log(data)
                if (tooltipItem.yLabel > 1000000) {
                  return '$' + Math.round(tooltipItem.yLabel/10000)/100 + 'M'
                }
                return '$' + tooltipItem.yLabel
              },
              footer: function(tooltipItem, data) {
                let avgVal = '$' + stats.means[tooltipItem[0].index]
                if (stats.means[tooltipItem[0].index] > 1000000) {
                  avgVal = '$' + Math.round(stats.means[tooltipItem[0].index]/10000)/100 + 'M'
                }
                str = [
                  'Average Portfolio Value: ' + avgVal,
                  'Reached Target: ' + stats.success_rates[tooltipItem[0].index] + '%',
                ]
                return str
              }
            },
          },
      }
  });
}

function setupPreChart1(labels, counts, stats) {
  var ctx = document.getElementById("pre-chart1").getContext('2d');
  var preChart1 = new Chart(ctx, {
    type: 'bar',
    data: {
      datasets: [{
        label: '# of Simulations that Reached Target',
        data: counts,
        yAxisID: 'A',
        backgroundColor: '#3e95cd',
      }, {
        label: '% of Simulations that Reached Target',
        data: stats.success_rates.slice(labels[0], labels[labels.length - 1] + 1),
        yAxisID: 'B',
        type: 'line'
      }],
      labels: labels,
    },
    options: {
      scales: {
        xAxes: [{
          ticks: {
            callback: function(value, index, values) {
              return 'Year ' + value
            },
          }
        }],
        yAxes: [{
          id: 'A',
          type: 'linear',
          position: 'left',
        }, {
          id: 'B',
          type: 'linear',
          position: 'right',
          ticks: {
            max: 100,
            min: 0,
            callback: function(value, index, values) {
              return value + '%'
            },
          },
        }],
      },
    },
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

function setupPostChart0(labels, datasets, stats) {
  var ctx = document.getElementById("post-chart0").getContext('2d');
  var postChart0 = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: datasets,
      },
      options: {
          legend: {
            display: true,
            labels: {
              filter: function(item, chart) {
                //console.log(item)
                if (item.text == null) {
                  return null
                }
                else {
                  return item.text
                }
              },
            },
          },
          scales: {
            xAxes: [{
              ticks: {
                //maxTicksLimit: Math.round(labels.length / 5),
              }
            }],
            yAxes: [{
              type: 'linear',
              ticks: {
                // Include a dollar sign in the ticks
                callback: function(value, index, values) {
                  if (value >= 1000000) {
                    return '$' + Math.round(value/10000)/100 + 'M'
                  }
                  return '$' + value
                },
              },
            }],
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
            callbacks: {
              title: function(tooltipItem, data) {
                //console.log(tooltipItem)
                return 'Year ' + tooltipItem[0].index
              },
              label: function(tooltipItem, data) {
                //console.log(tooltipItem)
                //console.log(data)
                if (tooltipItem.yLabel > 1000000) {
                  return '$' + Math.round(tooltipItem.yLabel/10000)/100 + 'M'
                }
                return '$' + tooltipItem.yLabel
              },
              footer: function(tooltipItem, data) {
                let avgVal = '$' + stats.means[tooltipItem[0].index]
                if (stats.means[tooltipItem[0].index] > 1000000) {
                  avgVal = '$' + Math.round(stats.means[tooltipItem[0].index]/10000)/100 + 'M'
                }
                str = [
                  'Average Portfolio Value: ' + avgVal,
                  'Failed: ' + stats.failure_rates[tooltipItem[0].index] + '%',
                ]
                return str
              }
            },
          },
      }
  });
}

function setupPostChart1(labels, counts, success_rates) {
  var ctx = document.getElementById("post-chart1").getContext('2d');
  var postChart1 = new Chart(ctx, {
    type: 'bar',
    data: {
      datasets: [{
        label: '# of Failed Simulations',
        data: counts,
        yAxisID: 'A',
        backgroundColor: '#E60000',
      }, {
        label: '% of Surviving Simulations',
        data: success_rates.slice(labels[0], labels[labels.length - 1] + 1),
        yAxisID: 'B',
        type: 'line'
      }],
      labels: labels,
    },
    options: {
      scales: {
        xAxes: [{
          ticks: {
            callback: function(value, index, values) {
              return 'Year ' + value
            },
          }
        }],
        yAxes: [{
          id: 'A',
          type: 'linear',
          position: 'left',
        }, {
          id: 'B',
          type: 'linear',
          position: 'right',
          ticks: {
            max: 100,
            min: 0,
            callback: function(value, index, values) {
              return value + '%'
            },
          },
        }],
      },
    },
  });
}
