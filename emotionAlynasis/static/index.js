comdata = []
iddata = []
allscoredata = []
$.ajax({
    url: "http://172.16.20.218:5011/graph",
    type: "POST",
    dataType: "json",
    data: {'id': 0, 'name': "大盘"},
    success: function (data) {
        allscoredata = data.result[0]
    },
    error: function () {
    }
})

$.ajax({
    url: "http://172.16.20.218:5011/comdata",
    type: "get",
    dataType: "json",
    data: {
        userID: "1"
    },
    success: function (data) {
        comdata = data.result[0]
        iddata = data.result[1]
        for (var i=0;i<comdata.length;i++){
            $("#comSel").append("<option value=" + comdata[i] +">"+iddata[i]+"</option>");
            }
    },
    error: function () {
    }
})


$("#score").click(function() {
        postData = $('#sentence').val();
        ctg = $('select').val();
        if(ctg == 'comment'){
            url = "http://172.16.20.218:5011/alynasis";
        }else {
            url = "http://172.16.20.218:5011/newsalynasis"
        }
        $.ajax({
            type: "POST",
            url: url,
            data: {'sentence': postData},
            dataType: "json",
            success: function (data) {
                $('#result_baidu').text("百度评分："+ data.result[0])
                $('#result_model').text("模型打分：" + data.result[1])
                $('#result_tag').text("标签：" + data.result[2])
            }
        })
    }
)

var myChart = echarts.init(document.getElementById('main'));

$("#graphbutton").click(function(){
    debugger;
    $('#company_name')[0].value
    var name=$('#company_name')[0].value;
    var index = comdata.indexOf(name)
    var id=iddata[index];
            url2 = "http://172.16.20.218:5011/graph"
        $.ajax({
            type: "POST",
            url: url2,
            data: {'id': id, 'name': name},
            dataType: "json",
            success: function (data) {
                // console.log(data.result[0])
                myChart.setOption(option = {
                    title: {
                        text: name+'历史舆论'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    xAxis: {
                        data: data.result[1]
                    },
                    yAxis: {
                        splitLine: {
                            show: false
                        }
                    },
                    toolbox: {
                        left: 'center',
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    dataZoom: [{
                        startValue: '2017-12-31'
                    }, {
                        type: 'inside'
                    }],
                    visualMap: {
                        top: 10,
                        right: 10,
                        pieces: [{
                            gt: 0,
                            lte: 30,
                            color: '#096'
                        }, {
                            gt: 30,
                            lte: 50,
                            color: '#ffde33'
                        }, {
                            gt: 50,
                            lte: 60,
                            color: '#ff9933'
                        }, {
                            gt: 60,
                            lte: 80,
                            color: '#cc0033'
                        }, {
                            gt: 80,
                            lte: 100,
                            color: '#660099'
                        }],
                        // outOfRange: {
                        //     color: '#999'
                        // }
                    },
                    series: [{
                        name: name+'历史舆论',
                        type: 'line',
                        data: data.result[0],
                        markLine: {
                            silent: true,
                            data: [{
                                yAxis: 50
                            },  {
                                yAxis: 60
                            },  {
                                yAxis: 80
                            }]
                        }
                    },{
                        name: '大盘历史舆论',
                        type: 'line',
                        data: allscoredata,
                        markLine: {
                            silent: true,
                            data: [{
                                yAxis: 50
                            },  {
                                yAxis: 60
                            },  {
                                yAxis: 80
                            }]
                        }
                    }],
                });
            }
        })
})

// $("#graph").click(function() {
//         url = "http://172.16.20.218:5011/graph"
//         $.ajax({
//             type: "POST",
//             url: url,
//             data: {'id': 2, 'name': '人众金服'},
//             dataType: "json",
//             success: function (data) {
//                 console.log(data.result[0])
//                 myChart.setOption(option = {
//                     title: {
//                         text: 'Beijing AQI'
//                     },
//                     tooltip: {
//                         trigger: 'axis'
//                     },
//                     xAxis: {
//                         data: data.result[1]
//                     },
//                     yAxis: {
//                         splitLine: {
//                             show: false
//                         }
//                     },
//                     toolbox: {
//                         left: 'center',
//                         feature: {
//                             dataZoom: {
//                                 yAxisIndex: 'none'
//                             },
//                             restore: {},
//                             saveAsImage: {}
//                         }
//                     },
//                     dataZoom: [{
//                         startValue: '2014-06-01'
//                     }, {
//                         type: 'inside'
//                     }],
//                     visualMap: {
//                         top: 10,
//                         right: 10,
//                         pieces: [{
//                             gt: 0,
//                             lte: 30,
//                             color: '#096'
//                         }, {
//                             gt: 30,
//                             lte: 50,
//                             color: '#ffde33'
//                         }, {
//                             gt: 50,
//                             lte: 60,
//                             color: '#ff9933'
//                         }, {
//                             gt: 60,
//                             lte: 80,
//                             color: '#cc0033'
//                         }, {
//                             gt: 80,
//                             lte: 100,
//                             color: '#660099'
//                         }, {
//                             gt: 100,
//                             color: '#7e0023'
//                         }],
//                         outOfRange: {
//                             color: '#999'
//                         }
//                     },
//                     series: {
//                         name: 'Beijing AQI',
//                         type: 'line',
//                         data: data.result[0],
//                         markLine: {
//                             silent: true,
//                             data: [{
//                                 yAxis: 50
//                             },  {
//                                 yAxis: 80
//                             }]
//                         }
//                     }
//                 });
//             }
//         })
//     }
// )
