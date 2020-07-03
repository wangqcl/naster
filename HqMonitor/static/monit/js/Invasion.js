//主要受攻击端口
function in_ap(nu_port,nu_values) {
    var myChart = echarts.init(document.getElementById('inap'));
    var imgUrl = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJsAAACZCAYAAAA4qUiHAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA3hpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDoyMjI0ZDUzMi0wZGI3LTQ5M2YtYWQyMy0xMmFkOTBiYmY2NTYiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6M0JENTEwREQxODBCMTFFQUFBRDBFQzQ5REMzNDI0QTIiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6M0JENTEwREMxODBCMTFFQUFBRDBFQzQ5REMzNDI0QTIiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKE1hY2ludG9zaCkiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoxZTliZmM5ZS0wNGNhLTQ2NGMtODI5Ny1hN2JiM2E5ODRkM2IiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MjIyNGQ1MzItMGRiNy00OTNmLWFkMjMtMTJhZDkwYmJmNjU2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";

    option = {
        //backgroundColor: '#043e9e',
        tooltip: {
            trigger: 'item',
            axisPointer: {
                type: 'shadow',
            },
            textStyle: {
                fontSize: 14,
            },
            formatter: "{a} <br/>{b}: {c}({d}%)",
        },
        graphic: {
            elements: [{
                type: 'image',
                style: {
                    image: imgUrl,
                    width: 180,
                    height: 180
                },
                left: 'center',
                top: 'center'
            }]
        },
        title: {
            text: '受攻击端口\n\n占比分析',
            x: 'center',
            y: 'center',
            textStyle: {
                width:50,
                color: '#fff',
                fontSize: 14
            }

        },
        legend: {
            show: true,
            left: "left",
            top: 10,
            orient: "vertical",
            textStyle: {
                color: '#ffffff',
                fontStyle: 'normal',
                fontSize: 14,
            },
            data: nu_port
        },
        color: ['#01ffc4', '#f2e224', '#00dcf8', '#0475bd'],
        series: [
            // 数据展示层
            {
                name: '受攻击端口占比分析',
                type: 'pie',
                center: ['50%', '50%'],
                radius: ['50%', '65%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: true,
                        position: 'outside',
                        formatter: (params)=>{
                            return '{b| '+params.name+'}{c|:'+params.value+'}\n' + '{c|'+params.percent.toFixed(0)+'%}'
                        },
                        padding: [0, -90],
                        align: 'center',
                        rich: {
                            b: {
                                fontSize: 18,
                                padding:[2,0]
                            },
                            c: {
                                fontSize: 16,
                                fontWeight:'bold',
                                align:'right',
                                padding:[2,0]
                            }
                        }
                    },
                    emphasis: {
                        show: false,
                        textStyle: {
                            fontSize: 14,
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: true,
                        length2:175
                    }
                },
                data: nu_values
            },
            // 外边框虚线
            {
                type: 'pie',
                zlevel: 4,
                silent: true,
                radius: ['75%', '76%'],
                label: {
                    normal: {
                        show: false
                    },
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: createData()
            },
        ]
    };
    function createData() {
        let dataArr = [];
        for(var i = 0; i < 200; i++) {
            if(i % 2 === 0) {
                dataArr.push({
                    //name: (i + 1).toString(),
                    value: 25,
                    itemStyle: {
                        normal: {
                            color: "#0475bd",
                            borderWidth: 0,
                            borderColor: "rgba(0,0,0,0)"
                        }
                    }
                })
            } else {
                dataArr.push({
                    //name: (i + 1).toString(),
                    value: 20,
                    itemStyle: {
                        normal: {
                            color: "rgba(0,0,0,0)",
                            borderWidth: 0,
                            borderColor: "rgba(0,0,0,0)"
                        }
                    }
                })
            }

        }
        return dataArr
    }
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
            fontSize: 100/1,
            color: '#00ffff',
            fontWeight: '500',
            padding: [-150, 0, 0, 0]
        },
        bule: {
            fontSize:100/1,
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
                fontSize: 8,
                fontFamily: 'Microsoft YaHei',
                color: '#fff'
            },
            type: 'category',
            nameLocation: 'end',
            nameGap: 8,
            axisLabel: {
                fontSize: 10,
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
    myChart.clear()
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



