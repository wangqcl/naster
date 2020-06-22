//主要威胁IP分值
function ec_mainthr(tiv_xdata,tiv_ydata) {
    var myChart = echarts.init(document.getElementById('mainthr'));

    var myColor = ['#33FFCC', '#33CCFF', '#0096f3', '#00c0e9', '#00e9db', '#34da62', '#d0a00e','#eb2100', '#eb3600', '#d0570e'];
    option = {
        // backgroundColor: '#0e2147',
        grid: {
            left: '11%',
            top: '5%',
            right: '0%',
            bottom: '8%',
            containLabel: true
        },
        xAxis: [{
            show: false,
        }],
        yAxis: [{
            axisTick: 'none',
            axisLine: 'none',
            offset: '27',  //距离图距离
            axisLabel: {
                textStyle: {
                    color: 'rgba(255,255,255,.6)',
                    fontSize: '16',
                }
            },
            data: tiv_xdata,//['南昌转运中心', '广州转运中心', '杭州转运中心', '宁夏转运中心', '兰州转运中心', '南宁转运中心', '长沙转运中心', '武汉转运中心', '合肥转运中心', '贵州转运中心']
        }, {
            axisTick: 'none',
            axisLine: 'none',
            axisLabel: {
                textStyle: {
                    color: '#ffffff',
                    fontSize: '16',
                }
            },
            data: ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
        }, {
            name: '分拨延误TOP 10',
            nameGap: '50',
            nameTextStyle: {
                color: '#ffffff',
                fontSize: '16',
            },
            axisLine: {
                lineStyle: {
                    color: 'rgba(0,0,0,0)'
                }
            },
            data: [],
        }],
        series: [{
                name: '条',
                type: 'bar',
                yAxisIndex: 0,
                data: tiv_ydata,//[4, 13, 25, 29, 38, 44, 50, 52, 60, 72],
                label: {
                    normal: {
                        show: true,
                        position: 'right',
                        textStyle: {
                            color: '#ffffff',
                            fontSize: '16',
                        }
                    }
                },
                barWidth: 5,
                itemStyle: {
                    normal: {
                        color: function(params) {
                            var num = myColor.length;
                            return myColor[params.dataIndex % num]
                        },
                    }
                },
                z: 2
            }, {
                name: '白框',
                type: 'bar',
                yAxisIndex: 1,
                barGap: '-100%',
                data: [99, 99.5, 99.5, 99.5, 99.5, 99.5, 99.5, 99.5, 99.5, 99.5],
                barWidth: 20,
                itemStyle: {
                    normal: {
                        color: '#095785',
                        barBorderRadius: 5,
                    }
                },
                z: 1
            }, {
                name: '外框',
                type: 'bar',
                yAxisIndex: 2,
                barGap: '-100%',
                data: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                barWidth: 24,
                itemStyle: {
                    normal: {
                        color: function(params) {
                            var num = myColor.length;
                            return myColor[params.dataIndex % num]
                        },
                        barBorderRadius: 5,
                    }
                },
                z: 0
            },
            {
                name: '外圆',
                type: 'scatter',
                hoverAnimation: false,
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                yAxisIndex: 2,
                symbolSize: 25,
                itemStyle: {
                    normal: {
                        color: function(params) {
                            var num = myColor.length;
                            return myColor[params.dataIndex % num]
                        },
                        opacity: 1,
                    }
                },
                z: 2
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
}

//总威胁趋势
function ec_totalthr(times,values) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('totalthr'));
        option = {
          tooltip: { //鼠标移上去显示的内容
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#dddc6b'  //竖线颜色
              }
            }
          },
          legend: {
            top: '0%',
            data: ['数量'],
            textStyle: {
              color: 'rgba(255,255,255,.5)', //图标颜色
              fontSize: '12', //图表字体
            }
          },
          grid: {
            left: '10',
            top: '30',
            right: '10',
            bottom: '10',
            containLabel: true
          },

          xAxis: [{
            type: 'category',
            boundaryGap: false,
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",//X坐标颜色
                fontSize: 12,
              },
            },
            axisLine: {
              lineStyle: {//X轴线颜色
                color: 'rgba(255,255,255,.2)'
              }
            },

            // data: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
            data:times
          }, {

            axisPointer: {show: false},
            axisLine: {show: false},
            position: 'bottom',
            offset: 20,


          }],

          yAxis: [{
            type: 'value',
            axisTick: {show: false},
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            },
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize: 12,
              },
            },

            splitLine: { //设置分隔线样式，也可以直接不显示
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              },
            }
          }],
          series: [
            {
              name: 'count',
              type: 'line',
              //smooth: true, //线性属性
              symbol: 'circle',
              symbolSize: 5,
              showSymbol: false,
              lineStyle: {
                normal: {//控制线颜色
                  color: '#00d887',
                  width: 2
                }
              },
              areaStyle: {//渐变颜色
                normal: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 216, 135, 0.4)'
                  }, {
                    offset: 0.8,
                    color: 'rgba(0, 216, 135, 0.1)'
                  }], false),
                  shadowColor: 'rgba(0, 0, 0, 0.1)',
                }
              },
              itemStyle: { //控制线图表颜色
                normal: {
                  color: '#00d887',
                  borderColor: 'rgba(221, 220, 107, .1)',
                  borderWidth: 12
                }
              },
              // data: [5, 3, 5, 6, 1, 5, 3, 5, 6, 4, 6, 4, 8, 3, 5, 6, 1, 5, 3, 7, 2, 5, 1, 4]
              data: values
            },

          ]

        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
        myChart.resize();
      }

//TI威胁趋势
function ec_tithr(ti_times,ti_values) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('tithr'));
        option = {
          tooltip: { //鼠标移上去显示的内容
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#dddc6b'  //竖线颜色
              }
            }
          },
          legend: {
            top: '0%',
            data: ['数量'],
            textStyle: {
              color: 'rgba(255,255,255,.5)', //图标颜色
              fontSize: '12', //图表字体
            }
          },
          grid: {
            left: '10',
            top: '30',
            right: '10',
            bottom: '10',
            containLabel: true
          },

          xAxis: [{
            type: 'category',
            boundaryGap: false,
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",//X坐标颜色
                fontSize: 12,
              },
            },
            axisLine: {
              lineStyle: {//X轴线颜色
                color: 'rgba(255,255,255,.2)'
              }
            },

            // data: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
            data:ti_times
          }, {

            axisPointer: {show: false},
            axisLine: {show: false},
            position: 'bottom',
            offset: 20,


          }],

          yAxis: [{
            type: 'value',
            axisTick: {show: false},
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            },
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize: 12,
              },
            },

            splitLine: { //设置分隔线样式，也可以直接不显示
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              },
            }
          }],
          series: [
            {
              name: 'count',
              type: 'line',
              //smooth: true, //线性属性
              symbol: 'circle',
              symbolSize: 5,
              showSymbol: false,
              lineStyle: {
                normal: {//控制线颜色
                  color: '#FF5722',
                  width: 2
                }
              },
              areaStyle: {//渐变颜色
                normal: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(255,87,34, 0.4)'
                  }, {
                    offset: 0.8,
                    color: 'rgba(255,87,34, 0.1)'
                  }], false),
                  shadowColor: 'rgba(0, 0, 0, 0.1)',
                }
              },
              itemStyle: { //控制线图表颜色
                normal: {
                  color: '#FF5722',
                  borderColor: 'rgba(221, 220, 107, .1)',
                  borderWidth: 12
                }
              },
              // data: [5, 3, 5, 6, 1, 5, 3, 5, 6, 4, 6, 4, 8, 3, 5, 6, 1, 5, 3, 7, 2, 5, 1, 4]
              data: ti_values
            },

          ]

        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
        myChart.resize();
      }

//WEB威胁安全趋势
function ec_webthr(we_times,we_values) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('webthr'));
        option = {
          tooltip: { //鼠标移上去显示的内容
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#dddc6b'  //竖线颜色
              }
            }
          },
          legend: {
            top: '0%',
            data: ['数量'],
            textStyle: {
              color: 'rgba(255,255,255,.5)', //图标颜色
              fontSize: '12', //图表字体
            }
          },
          grid: {
            left: '10',
            top: '30',
            right: '10',
            bottom: '10',
            containLabel: true
          },

          xAxis: [{
            type: 'category',
            boundaryGap: false,
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",//X坐标颜色
                fontSize: 12,
              },
            },
            axisLine: {
              lineStyle: {//X轴线颜色
                color: 'rgba(255,255,255,.2)'
              }
            },

            // data: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
            data:we_times
          }, {

            axisPointer: {show: false},
            axisLine: {show: false},
            position: 'bottom',
            offset: 20,


          }],

          yAxis: [{
            type: 'value',
            axisTick: {show: false},
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            },
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize: 12,
              },
            },

            splitLine: { //设置分隔线样式，也可以直接不显示
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              },
            }
          }],
          series: [
            {
              name: 'count',
              type: 'line',
              //smooth: true, //线性属性
              symbol: 'circle',
              symbolSize: 5,
              showSymbol: false,
              lineStyle: {
                normal: {//控制线颜色
                  color: '#01AAED',
                  width: 2
                }
              },
              areaStyle: {//渐变颜色
                normal: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(1,170,237, 0.4)'
                  }, {
                    offset: 0.8,
                    color: 'rgba(1,170,237, 0.1)'
                  }], false),
                  shadowColor: 'rgba(0, 0, 0, 0.1)',
                }
              },
              itemStyle: { //控制线图表颜色
                normal: {
                  color: '#01AAED',
                  borderColor: 'rgba(221, 220, 107, .1)',
                  borderWidth: 12
                }
              },
              // data: [5, 3, 5, 6, 1, 5, 3, 5, 6, 4, 6, 4, 8, 3, 5, 6, 1, 5, 3, 7, 2, 5, 1, 4]
              data: we_values
            },

          ]

        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
        myChart.resize();
      }

//入侵检测威胁趋势
function ec_inthr(in_times,in_values) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('inthr'));
        option = {
          tooltip: { //鼠标移上去显示的内容
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#dddc6b'  //竖线颜色
              }
            }
          },
          legend: {
            top: '0%',
            data: ['数量'],
            textStyle: {
              color: 'rgba(255,255,255,.5)', //图标颜色
              fontSize: '12', //图表字体
            }
          },
          grid: {
            left: '10',
            top: '30',
            right: '10',
            bottom: '10',
            containLabel: true
          },

          xAxis: [{
            type: 'category',
            boundaryGap: false,
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",//X坐标颜色
                fontSize: 12,
              },
            },
            axisLine: {
              lineStyle: {//X轴线颜色
                color: 'rgba(255,255,255,.2)'
              }
            },

            // data: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
            data:in_times
          }, {

            axisPointer: {show: false},
            axisLine: {show: false},
            position: 'bottom',
            offset: 20,


          }],

          yAxis: [{
            type: 'value',
            axisTick: {show: false},
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            },
            axisLabel: {
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize: 12,
              },
            },

            splitLine: { //设置分隔线样式，也可以直接不显示
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              },
            }
          }],
          series: [
            {
              name: 'count',
              type: 'line',
              //smooth: true, //线性属性
              symbol: 'circle',
              symbolSize: 5,
              showSymbol: false,
              lineStyle: {
                normal: {//控制线颜色
                  color: '#00ffff',
                  width: 2
                }
              },
              areaStyle: {//渐变颜色
                normal: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0,255,255, 0.4)'
                  }, {
                    offset: 0.8,
                    color: 'rgba(0,255,255, 0.1)'
                  }], false),
                  shadowColor: 'rgba(0, 0, 0, 0.1)',
                }
              },
              itemStyle: { //控制线图表颜色
                normal: {
                  color: '#00ffff',
                  borderColor: 'rgba(221, 220, 107, .1)',
                  borderWidth: 12
                }
              },
              // data: [5, 3, 5, 6, 1, 5, 3, 5, 6, 4, 6, 4, 8, 3, 5, 6, 1, 5, 3, 7, 2, 5, 1, 4]
              data: in_values
            },

          ]

        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
        myChart.resize();
      }

