//请求数量折线图
function echarts_4(times,values) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart4'));
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
              data:values
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

function echarts_34(nu_port,nu_values) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart1_1'));
        option = {

            title: [{
                text: '主要访问端口',
                left: 'center',
                textStyle: {
                    color: '#83c3e3',
                    fontSize: '16'
                }
            }],
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)",
                position: function (p) {   //其中p为当前鼠标的位置
                    return [p[0] + 10, p[1] - 10];
                }
            },
            legend: {

                //top: '70%',
                x : 'center',
                y : 'bottom',
                itemWidth: 10,
                itemHeight: 10,
                data: nu_port, //[80, 443, 8889, 3306, 21],//下方展示数据
                textStyle: {
                    color: 'rgba(255,255,255,.5)',
                    fontSize: '12',
                }
            },
            series: [
                {
                    name: '端口占比',
                    type: 'pie',
                    center: ['50%', '42%'],
                    radius: ['40%', '60%'],
                    color: ['#065aab', '#066eab', '#0682ab', '#0696ab', '#06a0ab', '#06b4ab', '#06c8ab', '#06dcab', '#06f0ab'],
                    label: {show: false},
                    labelLine: {show: false},
                    data:nu_values
                    // data: [
                    //     {'value': 11, 'name': 80},//value是数量
                    //     {value: 4, name: 443},
                    //     {value: 2, name: 8889},
                    //     {value: 2, name: 3306},
                    //     {value: 1, name: 21},
                    // ]
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

function echarts_35(st_series,st_port_data,st_xAxis_data) {
        var myChart = echarts.init(document.getElementById('echart1_2'));
        option = {
            color : ['#0E7CE2', '#FF8352', '#E271DE', '#F8456B', '#00FFFF', '#4AEAB0'],
            title: [{
                text: '服务器状态码',
                left: 'center',
                textStyle: {
                    color: '#83c3e3',
                    fontSize: '16'
                }
            }],
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            legend: {
                x : 'center',
                y : 'bottom',
                data: st_port_data,
                textStyle: {
                  color: 'rgba(255,255,255,.5)', //图标颜色
                  fontSize: '12', //图表字体
                }
            },
            grid: {//echart位置
                left: '3%',
                right: '4%',
                bottom: '20%',
                top: '11%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: st_xAxis_data,
                    axisLabel: {
                      textStyle: {
                        color: "rgba(255,255,255,.6)",//X坐标颜色
                        fontSize: 12,
                      },
                    },
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    axisLabel: {
                      textStyle: {
                        color: "rgba(255,255,255,.6)",//X坐标颜色
                        fontSize: 12,
                      },
                    },
                    splitLine: { //分隔线样式
                      lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                      }
                    }
                }
            ],
            // data
            series: st_series
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

function echarts_2(do_series,do_port_data,do_xAxis_data) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart2'));

        option = {
            // title: {
            //     text: '堆叠区域图'
            // },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#6a7985'
                    }
                }
            },
            legend: {
                x : 'center',
                y : 'bottom',
                data: [],//do_port_data,
                textStyle: {
                  color: 'rgba(0,0,0,.5)', //图表字体颜色和透明度
                  fontSize: '12', //图表字体
                }
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '20%',
                top: '11%',
                containLabel: true

            },
            xAxis: [
                {
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
                    data: do_xAxis_data
                }
            ],
            yAxis: [
                {
                    type: 'value',
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
                        splitLine: { //设置分隔线样式，也可以直接不显示
                            lineStyle: {
                            color: 'rgba(255,255,255,.1)'
                        },
                        }
                }
            ],
            series: do_series
        };



        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

function echarts_5(fa_ip,fa_values) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart5'));

        option = {
            //  backgroundColor: '#00265f',
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },

            grid: {
                left: '0%',
                top: '10px',
                right: '0%',
                bottom: '2%',
                containLabel: true
            },
            xAxis: [{
                type: 'category',
                data: fa_ip,//['浙江', '上海', '江苏', '广东', '北京', '深圳', '安徽', '四川'],
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: "rgba(255,255,255,.1)",
                        width: 1,
                        type: "solid"
                    },
                },
                axisLabel: {
                      textStyle: {
                        color: "rgba(255,255,255,.6)",//X坐标颜色
                        fontSize: 12,
                      },
                    },

                axisTick: {
                    show: false,
                },
            }],
            yAxis: [{
                type: 'value',
                axisLabel: {
                    //formatter: '{value} %'
                    show: true,
                    textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: '12',
                    },
                },
                axisTick: {
                    show: false,
                },
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: "rgba(255,255,255,.1	)",
                        width: 1,
                        type: "solid"
                    },
                },
                splitLine: {
                    lineStyle: {
                        color: "rgba(255,255,255,.1)",
                    }
                }
            }],
            series: [{
                type: 'bar',
                data: fa_values,//[2, 3, 3, 9, 15, 12, 6, 4, 6, 7, 4, 10],
                barWidth: '30%', //柱子宽度

                markLine: {
                // symbol: ['none'],//去掉箭头
                itemStyle: {
                    normal: { lineStyle: { type: 'solid', color:'#928ea8'}
                    ,label: { show: false, position:'left' } }
                },
                data: [{
                        name: 'Y 轴值为 60 的水平线',
                        yAxis: 60,
                },
                ]
        },
                // barGap: 1, //柱子之间间距
                itemStyle: { //添加随机的颜色
                        normal: {
                            color: function(params) {
                                // build a color map as your need.
                                var colorList = [
                                    '#bcd3bb', '#e88f70', '#9dc5c8', '#e1e8c8',
                                    '#7b7c68', '#e5b5b5', '#f0b489', '#928ea8',
                                    '#bda29a', '#376956', '#c3bed4', '#495a80',
                                    '#9966cc', '#bdb76a', '#eee8ab', '#a35015',
                                    '#04dd98', '#d9b3e6', '#b6c3fc','#315dbc',
                                ];
                                return colorList[params.dataIndex]
                            },
                        }
                    },
            }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

function echarts_31(rq_series,rq_port_data,rq_xAxis_data) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('fb1'));
    option = {
        title: [{
            text: '客户端请求流量',
            left: 'center',
            textStyle: {
                color: '#83c3e3',
                fontSize: '16'
            }
        }],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
            x : 'center',
            y : 'bottom',
            data: [],//do_port_data,
            textStyle: {
              color: 'rgba(0,0,0,.5)', //图表字体颜色和透明度
              fontSize: '12', //图表字体
            }
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '20%',
            top: '11%',
            containLabel: true

        },
        xAxis: [
            {
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
                data: rq_xAxis_data,
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                  formatter:'{value}(kb)',
                  textStyle: {
                    color: "rgba(255,255,255,.6)",//X坐标颜色
                    fontSize: 12,
                    formatter:'t'
                  },
                },
                axisLine: {
                  lineStyle: {//X轴线颜色
                    color: 'rgba(255,255,255,.2)'
                  }
                },
                    splitLine: { //设置分隔线样式，也可以直接不显示
                        lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                    },
                    }
            }
        ],
        series: rq_series,
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
}
//客户端响应流量
function echarts_32(lineY,charts) {
        var myChart = echarts.init(document.getElementById('fb2'));

        option = {
             title: [{
                text: '客户端响应流量',
                left: 'center',
                textStyle: {
                    color: '#83c3e3',
                    fontSize: '16'
                }
            }],
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: charts.names,
                textStyle: {
                    fontSize: 5,//标识大小
                    color: 'rgb(0,253,255,0.6)'
                },
                right: '4%',
                top: '4%',
            },
            grid: {
                top: '14%',
                left: '4%',
                right: '4%',
                bottom: '12%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: charts.lineX,
                axisLabel: {
                    textStyle: {
                        color: 'rgba(255,255,255,.6)'
                    },
                    formatter: function(params) {
                        return params.split(' ')[0] + '\n' + params.split(' ')[1]
                    }
                }
            },
            yAxis: {
                name: charts.unit,
                type: 'value',
                axisLabel: {
                    formatter: '{value}',
                    textStyle: {
                        color: 'rgba(255,255,255,.6)'
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgb(23,255,243,0.3)'
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgb(0,253,255,0.6)'
                    }
                }
            },
            series: lineY
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

function echarts_44(linesY,wcharts) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echart44'));

        option = {
            tooltip: {
            trigger: 'axis',
            axisPointer: {
                lineStyle: {
                    color: '#dddc6b'
                }
            }
        },
                legend: {
                    top:'0%',
                        data:wcharts.names,
                        textStyle: {
                           color: 'rgba(255,255,255,.5)',
                            fontSize:'12',
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
            axisLabel:  {
                            textStyle: {
                                color: "rgba(255,255,255,.6)",
                                fontSize:12,
                            },
                        },
            axisLine: {
                lineStyle: {
                    color: 'rgba(255,255,255,.2)'
                }
            },
            data: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
            }, {
                axisPointer: {show: false},
                axisLine: {  show: false},
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
           axisLabel:  {
                    textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize:12,
                    },
                },

            splitLine: {
                lineStyle: {
                     color: 'rgba(255,255,255,.1)'
                }
            }
        }],
        series: linesY

};

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }

//世界地图
function word_map(geoCoordMap,BJData) {
    var myChart = echarts.init(document.getElementById('wordmap'));
        // function randomData() {
        //     return Math.round(Math.random() * 300);
        // }

var geoCoordMap = geoCoordMap;
var BJData = BJData;
var convertData = function(data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var dataItem = data[i];
        var fromCoord = geoCoordMap[dataItem[0].name];
        var toCoord = geoCoordMap[dataItem[1].name];
        if (fromCoord && toCoord) {
            res.push([{
                    coord: fromCoord,
                    value: dataItem[0].value
                },
                {
                    coord: toCoord
                }
            ]);
        }
    }
    return res;
};
var convertData2 = function(data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var dataItem = data[i];
        var fromCoord = geoCoordMap[dataItem[1].name];
        var toCoord = geoCoordMap[dataItem[0].name];
        if (fromCoord && toCoord) {
            res.push([{
                    coord: fromCoord,
                    value: dataItem[0].value
                },
                {
                    coord: toCoord
                }
            ]);
        }
    }
    return res;
};

var series = [];
[
    ["北京", BJData]
].forEach(function(item, i) {
    series.push({
            // name: '攻击线1',
            type: "lines",
            zlevel: 2,
            effect: {
                show: true,
                color: "#0bc7f3",
                period: 4, //箭头指向速度，值越小速度越快
                trailLength: 0.02, //特效尾迹长度[0,1]值越大，尾迹越长重
                symbol: "arrow", //箭头图标
                symbolSize: 5 //图标大小
            },
            lineStyle: {
                normal: {
                    color: '#0bc7f3',
                    width: 1, //尾迹线条宽度
                    opacity: 0, //尾迹线条透明度
                    curveness: 0.3 //尾迹线条曲直度
                }
            },
            data: convertData(item[1])
        },
        {

            type: "effectScatter",
            coordinateSystem: "geo",
            zlevel: 2,
            rippleEffect: {
                //涟漪特效
                period: 4, //动画时间，值越小速度越快
                brushType: "stroke", //波纹绘制方式 stroke, fill
                scale: 4 //波纹圆环最大限制，值越大波纹越大
            },
            label: {
                normal: {
                    show: true,
                    position: "right", //显示位置
                    offset: [5, 0], //偏移设置
                    formatter: "" //圆环显示文字"{b}"
                },
                emphasis: {
                    show: true,
                    color: "#FF6A6A"
                }
            },
            symbol: "circle",
            symbolSize: function(val) {
                return 8 + val[2] / 1000/10; //圆环大小
            },
            itemStyle: {
                normal: {
                    show: true,
                },
                emphasis: {
                    show: true,
                    color: "#FF6A6A"
                }
            },
            data: item[1].map(function(dataItem) {
                return {
                    name: dataItem[0].name,
                    value: geoCoordMap[dataItem[0].name].concat([dataItem[0].value]),
                };
            })
        },
        //被攻击点
        {
            type: "scatter",
            coordinateSystem: "geo",
            zlevel: 2,
            rippleEffect: {
                period: 4,
                brushType: "stroke",
                scale: 4
            },
            label: {
                normal: {
                    show: true,
                    color: "red",
                    position: "right",
                    formatter: "{b}",
                },
                emphasis: {
                    show: true,
                    color: "#FF6A6A"
                }
            },
            symbol: "pin",
            symbolSize: 30,
            itemStyle: {
                normal: {
                    show: true,
                    color: "red",
                },
                emphasis: {
                    show: true,
                    color: "#FF6A6A"
                }
            },
            data: [{
                name: item[0],
                value: geoCoordMap[item[0]].concat([100]),
                visualMap: false
            }]
        }
    );
});
var svg = "path://M32.597,9.782 L30.475,11.904 C30.085,12.294 29.452,12.294 29.061,11.904 C28.671,11.513 28.671,10.880 29.061,10.489 L31.182,8.368 C31.573,7.978 32.206,7.978 32.597,8.368 C32.987,8.759 32.987,9.392 32.597,9.782 ZM30.000,30.500 C30.000,31.328 29.329,32.000 28.500,32.000 L5.500,32.000 C4.672,32.000 4.000,31.328 4.000,30.500 C4.000,29.672 4.672,29.000 5.500,29.000 L8.009,29.000 L8.009,18.244 C8.009,13.139 12.034,9.000 17.000,9.000 C21.966,9.000 25.992,13.139 25.992,18.244 L25.992,29.000 L28.500,29.000 C29.329,29.000 30.000,29.672 30.000,30.500 ZM17.867,14.444 L13.000,22.000 L17.000,22.000 L17.133,26.556 L21.000,20.000 L17.000,20.000 L17.867,14.444 ZM25.221,6.327 C25.033,6.846 24.459,7.113 23.940,6.924 C23.421,6.735 23.153,6.162 23.342,5.643 L24.368,2.823 C24.557,2.304 25.131,2.037 25.650,2.226 C26.169,2.415 26.436,2.989 26.248,3.508 L25.221,6.327 ZM17.000,5.000 C16.448,5.000 16.000,4.552 16.000,4.000 L16.000,1.000 C16.000,0.448 16.448,0.000 17.000,0.000 C17.552,0.000 18.000,0.448 18.000,1.000 L18.000,4.000 C18.000,4.552 17.552,5.000 17.000,5.000 ZM10.028,7.197 C9.509,7.386 8.935,7.118 8.746,6.599 L7.720,3.780 C7.532,3.261 7.799,2.687 8.318,2.498 C8.837,2.309 9.411,2.577 9.600,3.096 L10.626,5.915 C10.815,6.434 10.547,7.008 10.028,7.197 ZM3.354,12.268 L1.232,10.146 C0.842,9.756 0.842,9.123 1.232,8.732 C1.623,8.342 2.256,8.342 2.646,8.732 L4.768,10.854 C5.158,11.244 5.158,11.877 4.768,12.268 C4.377,12.658 3.744,12.658 3.354,12.268 Z"



        // 基于准备好的dom，初始化echarts实例
        // var myChart = echarts.init(document.getElementById('wordmap'));
        option = {
            // backgroundColor: '#3779a1',//背景颜色
            tooltip: {
                trigger: "item",
                backgroundColor: "#1540a1",
                borderColor: "#FFFFCC",
                showDelay: 0,
                hideDelay: 0,
                enterable: true,
                transitionDuration: 0,
                extraCssText: "z-index:100",
                formatter: function(params, ticket, callback) {
                    //根据业务自己拓展要显示的内容
                    var res = "";
                    var name =params.name; //获取当前点名字
                    var value = params.value[params.seriesIndex + 1];
                    res =
                        "<span style='color:#fff;'>" +
                        name +
                        "</span><br/>数据：" +
                        value;
                    return res;

                }
            },
            visualMap: {
                //图例值控制
                show: false,
                type: 'piecewise',
                pieces: [{
                        max: 80,
                        color: 'red'
                    },
                    {
                        min: 80,
                        max: 120,
                        color: 'yellow'
                    },
                    {
                        min: 120,
                        color: 'green'
                    }
                ],
                calculable: true,
            },
            geo: {
                map: "world",
                show: true,
                label: {
                    emphasis: {
                        show: false
                    }
                },
                roam: true, //是否允许缩放
                layoutCenter: ["50%", "50%"], //地图位置
                layoutSize: "160%",
                itemStyle: {
                    normal: {
                        show: 'true',
                        color: "#04284e", //地图背景色
                        borderColor: "#5bc1c9" //省市边界线
                    },
                    emphasis: {
                        show: 'true',
                        color: "rgba(37, 43, 61, .5)" //悬浮背景
                    }
                }
            },
            legend: {
                orient: 'vertical',
                top: '30',
                left: 'center',
                align: 'right',
                data: [{
                        name: '攻击线1',
                        icon: svg,
                    },
                    // {
                    //     name: '攻击线2',
                    //     icon: svg
                    // },
                ],
                textStyle: {
                    color: '#fff',
                    fontSize: 10,
                },
                itemWidth: 50,
                itemHeight: 30,
                selectedMode: 'multiple'
            },
            series: series
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }

		
		
		


		









