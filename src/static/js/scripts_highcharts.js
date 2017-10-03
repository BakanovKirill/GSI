var colors = ['#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9',
                '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1', '#2f7ed8',
                '#0d233a', '#8bbc21', '#910000', '#1aadce',  '#492970', '#f28f43',
                '#77a1e5', '#c42525', '#a6c96a', '#4572A7', '#AA4643', '#89A54E',
                '#80699B', '#3D96AE', '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92']

function getDataSeries() {
    // alert('getDataSeries: '+select_diagram);
    // alert('ts_subtitle: '+ts_subtitle);
    
    if (ts_data) {
        if (select_diagram == 'line') {
            var ts_series = [];
            var count_color = 0;
            var data_list = ts_data.split('$$$');

            for (var n = 1; n < data_list.length; n++) {
                // alert('$$$ getDataSeries: '+data_list[n]);

                var ts_select_name = '';
                var ts_select_data = [];
                var ts_select_subtitle = '';
                var ts_tmp_dict = {};

                
                // var ts_tmp_dict;
                var data_sub_list = data_list[n].split('$');

                // alert('getDataSeries L: '+data_sub_list[n]);

                for (var m = 0; m < data_sub_list.length; m++) {
                    var data_value = data_sub_list[m].split(',');
                    
                    ts_select_name = data_value[0] + '-' + data_value[1] + '-' + data_value[2];
                    ts_select_subtitle = data_value[0] + ', ';

                    // alert('$ data_value[3]: '+data_value[3]);
                    
                    // var tmp = [];
                    // tmp.push(Date.UTC(2010, parseInt(data_value[3]), parseInt(data_value[4])));
                    // tmp.push(parseFloat(data_value[5]));

                    var tmp = [
                        Date.UTC(2010, parseInt(data_value[3]), parseInt(data_value[4])),
                        parseFloat(data_value[5])
                    ];

                    ts_select_data.push(tmp);
                    
                    // tmp = '';
                    
                    // alert('tmp: '+tmp);
                    // alert('ts_select_data: '+ts_select_data);
                }

                // alert('NAME: '+ts_select_name);
                // alert('ts_select_data: '+ts_select_data);
                // alert('ts_select_subtitle: '+ts_select_subtitle);
                // var colors = ['#7cb5ec', '#434348', ]
                var cur_color;

                if (colors.indexOf(colors[count_color]) != -1) {
                    cur_color = colors[count_color]
                } else {
                    count_color = 0;
                    cur_color = colors[count_color]
                }
                
                ts_subtitle = ts_subtitle + ts_select_subtitle;
                ts_select_subtitle = '';
                ts_tmp_dict.name = ts_select_name;
                ts_tmp_dict.data = ts_select_data;
                ts_tmp_dict.color = colors[n];

                count_color++;

                // var ts_tmp_dict = {
                //     'name': ts_select_name,
                //     'data': ts_select_data
                // }

                ts_series.push(ts_tmp_dict);

                // alert('ts_series: '+ts_series);
                
                initHighchartsLine(ts_series);
            }
        }

        if (select_diagram == 'box') {
            var box_category = [];
            var ts_series_box = [];
            var data_list = ts_data.split('$$$');

            for (var n = 1; n < data_list.length; n++) {
                var tmp_name;
                // var tmp_data = [];
                var tmp_data_list = [];
                var tmp_tooltip = {};
                var ts_tmp_dict = {};
                


                var data_sub_list = data_list[n].split('$');

                for (var m = 0; m < data_sub_list.length; m++) {
                    // var tmp = [];
                    // var tmp_data_list = [];
                    var data_value = data_sub_list[m].split(',');

                    var date_tmp = data_value[1].split('/')
                    date_tmp.splice(2,1);
                    category_date = date_tmp.join('/')

                    box_category.push(category_date);
                    plotLines_value = data_value[2]
                    var date_aoi = data_value[1].split('/')

                    tmp_name = 'AOI: ' + data_value[0];
                    var tmp_data = [
                        parseFloat(data_value[3]),
                        parseFloat(data_value[4]),
                        parseFloat(data_value[5]),
                        parseFloat(data_value[6]),
                        parseFloat(data_value[7])
                    ];

                    // alert('tmp_data: '+tmp_data);

                    tmp_data_list.push(tmp_data);
                    tmp_tooltip.headerFormat = '<em><b>Year:</b> ' + date_aoi[2] + '</em><br/>';
                }

                ts_subtitle = tmp_name;
                ts_tmp_dict.name = ts_subtitle;
                ts_tmp_dict.data = tmp_data_list;
                ts_tmp_dict.tooltip = tmp_tooltip;

                ts_series_box.push(ts_tmp_dict);

                // alert('categories: '+box_category);

                // initHighchartsBox(box_category, ts_series_box);
            }
            initHighchartsBox(box_category, ts_series_box);
        }
        

        ts_subtitle = ts_subtitle.split(', ').filter(function (e, i, arr) {
                    return arr.lastIndexOf(e) === i;
                }).join(', ');
        ts_subtitle = 'AOI: ' + ts_subtitle.substring(0, ts_subtitle.length - 2);

        // alert('SERIES SIZE: '+ts_series.length);
        // alert('NAME 0: '+ts_series[0]['name']);
        // alert('DATA 0: '+ts_series[0]['data']);

        // alert('NAME 1: '+ts_series[1]['name']);
        // alert('DATA 1: '+ts_series[1]['data']);

        // alert('NAME 2: '+ts_series[2]['name']);
        // alert('DATA 2: '+ts_series[2]['data']);
    }
}

function initHighchartsLine(ts_series) {
    chartLine = Highcharts.chart('container_line', {
        chart: {
            type: 'spline'
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                month: '%e/%b'
            },
            title: {
                text: '<b>Date</b>'
            }
        },
        yAxis: {
            title: {
                text: '<b>'+ts_units+'</b>'
            },
            min: 0
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e/%b/%Y}: {point.y:.4f} '+ts_units
        },

        plotOptions: {
            spline: {
                marker: {
                    enabled: true
                }
            }
        },

        series: ts_series,
    });
}

function initHighchartsBox(categories, ts_series) {
    var plotLinesText = '<b>Mean value: '+plotLines_value+'</b>';

    Highcharts.chart('container_box', {
        chart: {
            type: 'boxplot'
        },

        title: {
            text: ''
        },

        legend: {
            enabled: false
        },

        xAxis: {
            categories: categories,
            title: {
                text: '<b>Date</b>'
            }
        },

        yAxis: {
            title: {
                text: '<b>'+ts_units+'</b>'
            },
            plotLines: [{
                value: plotLines_value,
                color: 'red',
                width: 1,
                label: {
                    text: plotLinesText,
                    align: 'top',
                    style: {
                        color: 'gray'
                    }
                },
                zIndex: 5
            }]
        },

        series: ts_series
    });
}


$(document).ready(function(){
    if (ts_show) {
        getDataSeries();
    }
});
