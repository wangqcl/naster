//主要受攻击端口
function in_ap(nu_port,nu_values) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('inap'));
    var img = 'data:image/png;base64,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';

    var trafficWay = nu_values;

    var data = [];
    var color=['#00ffff','#00cfff','#006ced','#ffe000','#ffa800','#ff5b00','#ff3000']
    for (var i = 0; i < trafficWay.length; i++) {
        data.push({
            value: trafficWay[i].value,
            name: trafficWay[i].name,
            itemStyle: {
                normal: {
                    borderWidth: 5,
                    shadowBlur: 180,
                    borderColor:color[i],
                    shadowColor: color[i]
                }
            }
        }, {
            value: nu_values,
            name: '',
            itemStyle: {
                normal: {
                    label: {
                        show: false
                    },
                    labelLine: {
                        show: false
                    },
                    color: 'rgba(0, 0, 0, 0)',
                    borderColor: 'rgba(0, 0, 0, 0)',
                    borderWidth: 20
                }
            }
        });
    }
    var seriesOption = [{
        name: '',
        type: 'pie',
        clockWise: false,
        radius: [105, 109],
        hoverAnimation: false,
        itemStyle: {
            normal: {
                label: {
                    show: true,
                    position: 'outside',
                    color: '#ddd',
                    fontSize: 16,
                    formatter: function(params) {
                        var percent = 0;
                        var total = 0;
                        for (var i = 0; i < trafficWay.length; i++) {
                            total += trafficWay[i].value;
                        }
                        percent = ((params.value / total) * 100).toFixed(0);
                        if(params.name !== '') {
                            return '端口：' + params.name + '\n' + '\n' + '占百分比：' + percent + '%';
                        }else {
                            return '';
                        }
                    },
                },
                labelLine: {
                    length:30,
                    length2:20,
                    show: true,
                    color:'#00ffff'
                }
            }
        },
        data: data
    }];
    option = {
        //backgroundColor: '#0A2E5D',
        color : color,
        title: {
            text: '端口',
            top: '48%',
            textAlign: "center",
            left: "49%",
            textStyle: {
                color: '#fff',
                fontSize: 33,
                fontWeight: '400'
            }
        },
        graphic: {
            elements: [{
                type: "image",
                z: 3,
                style: {
                    image: img,
                    width: 278,
                    height: 278
                },
                left: 'center',
                top:  'center',
                position: [100, 100]
            }]
        },
        tooltip: {
            show: false
        },
        toolbox: {
            show: false
        },
        series: seriesOption
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
}

//总攻击数
function in_all(data) {
    var myChart = echarts.init(document.getElementById('inall'));
    var dataArr = [{
        value: data,
        name: '总攻击数'
    }];

    var rich = {
        white: {
            fontSize: 100,
            color: '#00ffff',
            fontWeight: '500',
            padding: [-150, 0, 0, 0]
        },
        bule: {
            fontSize: 200,
            fontFamily: 'DINBold',
            color: '#00ffff',
            fontWeight: '700',
            padding: [-120, 0, 0, 0],
        },
        radius: {
            width: 350,
            height: 80,
            // lineHeight:80,
            borderWidth: 1,
            borderColor: '#0092F2',
            fontSize: 50,
            color: '#fff',
            backgroundColor: '#1B215B',
            borderRadius: 20,
            textAlign: 'center',
        },
        size: {
            height: 400,
            padding: [100, 0, 0, 0]
        }
    }
    option = {
        //backgroundColor: '#0E1327',
        tooltip: {
            formatter: "{a} <br/>{b} : {c}%"
        },

        series: [
            {
                type: 'gauge',
                radius: '52%',
                startAngle: '225',
                endAngle: '-45',
                pointer: {
                    show: false
                },
                detail: {
                    formatter: function(value) {
                        var num = Math.round(value);
                        return '{bule|' + num + '}{white|次}' + '{size|' + '}\n\n\n';
                    },
                    rich: rich,
                    "offsetCenter": ['0%', "0%"],
                },
                data: dataArr,
                title: {
                    show: false,
                },
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#0E1327',
                        width: 25,
                        // shadowBlur: 15,
                        // shadowColor: '#B0C4DE',
                        shadowOffsetX: 0,
                        shadowOffsetY: 0,
                        opacity: 1
                    }
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    show: false,
                    length: 25,
                    lineStyle: {
                        color: '#0E1327',
                        width: 2,
                        type: 'solid',
                    },
                },
                axisLabel: {
                    show: false
                },
            },

        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });

}

//主要攻击类型攻击方式分类
function ac_cl(type,method,show) {
    var myChart = echarts.init(document.getElementById('accl'));
    option = {
        tooltip: {
            trigger: 'item',
        },
        series: [{
            name: '访问来源',
            type: 'pie',
            //selectedMode: 'single',
            radius: ['20%', '35%'],
            data: type
        },
            {
                name: '访问来源',
                type: 'pie',
                radius: ['40%', '55%'],
                data: method
            }
        ],
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
}

//主要攻击类型占比
function ac_ty(fa_ip,fa_values) {
    var myChart = echarts.init(document.getElementById('acty'));
    var sourceBar = {
        "itemData": fa_ip,
        "seriesData": fa_values
    }
    var itemData = sourceBar.itemData;
    var seriesData = sourceBar.seriesData;
    var tooltip = sourceBar.tooltip
    var color = ['#00b9f6', '#38a97d', '#004eff', '#17c7e7', '#4e85ea', '#e49be9', '#078d9d', '#eca52a', '#ef9544', '#ea3b3b']
    var data = {};
    for (var k in itemData) {
        data[itemData[k]] = seriesData[k];
    }

    var xAxisData = [];
    var dataArr = [];
    for (var i in data) {
        xAxisData.push(i);
        dataArr.push(data[i]);
    }

    option = {
        //backgroundColor: '#142058',
        grid: {
            top: '25%',
            left: '5%',
            right: '10%',
            bottom: '8%',
            containLabel: true
        },
        tooltip: {
            show: "true",
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                shadowStyle: {
                    color: 'rgba(112,112,112,0)',
                },
            },
            formatter: function(params) {
                var unit = params[0].name.substring(params[0].name.indexOf('(') + 1, params[0].name.indexOf(')'));
                return params[0].name + '：' + params[0].value + '条数据';
            },
            backgroundColor: 'rgba(0,0,0,0.7)', // 背景
            padding: [8, 10], //内边距
            extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影
        },
        xAxis: [{
            show: true,
            name: '来源',
            nameTextStyle: {
                fontSize: 14,
                fontFamily: 'Microsoft YaHei',
                color: '#fff'
            },
            type: 'category',
            nameLocation: 'end',
            nameGap: 8,
            axisLabel: {
                fontSize: 16,
                fontFamily: 'Microsoft YaHei',
                color: "#fff",
                interval: 0,
                margin: 16,
                formatter: function(params) {
                    if (params.length > 6) {
                        params = params.substr(0, 6) + "...";
                    } else {
                        params = params;

                    }
                    return params;
                }
            },
            axisLine: {
                show: true,
                symbol: ['none', 'arrow'],
                lineStyle: {
                    color: '#05edfc'
                }
            },
            data: xAxisData
        }, {
            type: 'category',
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                show: false
            },
            splitArea: {
                show: false
            },
            splitLine: {
                show: false
            },
            data: xAxisData
        }, {
            type: 'category',
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                show: false
            },
            splitArea: {
                show: false
            },
            splitLine: {
                show: false
            },
            data: xAxisData
        }],
        yAxis: {
            type: 'value',
            name: '数量',
            nameTextStyle: {
                fontSize: 14,
                fontFamily: 'Microsoft YaHei',
                color: '#fff'
            },
            minInterval: 1,
            nameLocation: 'end',
            nameGap: 10,
            splitLine: {
                show: false
            },
            axisLabel: {
                show: true,
                fontSize: 12,
                fontFamily: 'Arial',
                color: "#fff"
            },
            axisLine: {
                show: true,
                symbol: ['none', 'arrow'],
                lineStyle: {
                    color: '#05edfc'
                }
            }
        },
        series: [{
            type: 'bar',
            stack: 1,
            xAxisIndex: 0,
            barWidth: 10,
            barGap: 5,
            z: 2,
            data: function() {
                var itemArr = [];
                for (var i = 1; i < (dataArr.length + 1); i++) {
                    var item = {
                        value: dataArr[i - 1],
                        itemStyle: {
                            normal: {
                                barBorderRadius: 50,
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: color[translateColor(i) * 2 - 2]
                                }, {
                                    offset: 1,
                                    color: color[translateColor(i) * 2 - 1]
                                }]),
                            }
                        }
                    };
                    itemArr.push(item);
                }
                return itemArr;
            }()
        },
            {
                type: 'scatter',
                stack: 1,
                symbolOffset: [0, 0], //相对于原本位置的偏移量
                label: {
                    normal: {
                        show: false,
                    }
                },
                xAxisIndex: 2,
                symbolSize: 10,
                z: 2,
                data: function() {
                    var itemArr = [];
                    for (var i = 1; i < (dataArr.length + 1); i++) {
                        var item = {
                            value: 0,
                            itemStyle: {
                                normal: {
                                    borderColor: '#fff',
                                    borderWidth: 2,
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: color[translateColor(i) * 2 - 2]
                                    }, {
                                        offset: 1,
                                        color: color[translateColor(i) * 2 - 1]
                                    }]),
                                }
                            }
                        };
                        itemArr.push(item);
                    }
                    return itemArr;
                }()
            },
            {
                type: 'bar',
                xAxisIndex: 1,
                barGap: '140%',
                data: dataArr,
                barWidth: 22,
                itemStyle: {
                    normal: {
                        barBorderRadius: 50,
                        color: '#0e2147'
                    }
                },
                z: 1
            },
            {
                type: 'bar',
                xAxisIndex: 2,
                barWidth: 30,
                barGap: 1,
                z: 0,
                data: function() {
                    var itemArr = [];
                    for (var i = 1; i < (dataArr.length + 1); i++) {
                        var item = {
                            value: dataArr[i - 1],
                            itemStyle: {
                                normal: {
                                    barBorderRadius: 50,
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: color[translateColor(i) * 2 - 2]
                                    }, {
                                        offset: 1,
                                        color: color[translateColor(i) * 2 - 1]
                                    }]),
                                }
                            }
                        };
                        itemArr.push(item);
                    }
                    return itemArr;
                }()
            },
            {
                type: 'scatter',
                hoverAnimation: false,
                xAxisIndex: 2,
                symbolOffset: [0, 0], //相对于原本位置的偏移量
                symbolSize: 30,
                z: 2,
                data: function() {
                    var itemArr = [];
                    for (var i = 1; i < (dataArr.length + 1); i++) {
                        var item = {
                            value: 0,
                            itemStyle: {
                                normal: {
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: color[translateColor(i) * 2 - 2]
                                    }, {
                                        offset: 1,
                                        color: color[translateColor(i) * 2 - 1]
                                    }]),
                                }
                            }
                        };
                        itemArr.push(item);
                    }
                    return itemArr;
                }()
            }
        ]
    };

    function translateColor(index) {
        if (index > 5) {
            return translateColor(index - 5)
        }
        return index
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
}

//主要攻击类型
function ma_ac(name,linex,value){
    var myChart = echarts.init(document.getElementById('maac'));
    //var xData = ["2019-03-01", "2019-03-02", "2019-03-03", "2019-03-04", "2019-03-05", "2019-03-06", "2019-03-07", "2019-03-08", "2019-03-09", "2019-03-10", "2019-03-11", "2019-03-12", "2019-03-13", "2019-03-14", "2019-03-15", "2019-03-16", "2019-03-17", "2019-03-18", "2019-03-19", "2019-03-20"];
    var xData = linex;
    var yData = [10,20,30,40,50,60,70];
    option = {
        //backgroundColor: '#043491',
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            x: 'center',
            y: '40px',
            textStyle: {
                color: '#f2f2f2',
                fontSize: 13,
            },
            icon: 'circle',
            data: name
        },

        grid: {
            right: '5%',
            bottom: '10%',
            left: '2%',
            top: '80px',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            data: xData,
            nameTextStyle: {
                color: '#00b9f6'
            },
            axisLine: {
                lineStyle: {
                    color: '#00b9f6'
                }
            },
            axisTick: {
                show: false,
            },
            axisLabel: {
                show: true,
                textStyle: {
                    color: "#FFF",
                    fontSize: 12,
                },
                //interval:0,
                //rotate:30
            },
        }],
        yAxis: [{
            type: 'value',
            data: yData,
            nameTextStyle: {
                color: '#d4ffff'
            },
            position: 'left',
            axisLine: {
                lineStyle: {
                    color: '#00b9f6'
                }
            },
            splitLine: {
                lineStyle: {
                    color: "#0B4CA9",
                }

            },
            axisLabel: {
                color: '#d4ffff',
                fontSize: 12,
            }
        }, ],
        series: value
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
}