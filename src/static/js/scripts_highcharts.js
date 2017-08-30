function getDataSeries() {
    // alert('getDataSeries: '+ts_data);
    var data_list = ts_data.split('$$$');

    for (var n = 1; n < data_list.length; n++) {
        // alert('$$$ getDataSeries: '+data_list[n]);

        var ts_select_name = '';
        var ts_select_data = [];
        var ts_select_subtitle = '';
        // ts_subtitle = '';

        
        // var ts_tmp_dict;
        var data_sub_list = data_list[n].split('$');

        // alert('getDataSeries L: '+data_sub_list[n]);

        for (var m = 0; m < data_sub_list.length; m++) {
            // alert('$ getDataSeries: '+data_sub_list[m]);
            
            var data_value = data_sub_list[m].split(',');

            // var tmp = [
            //     Date.UTC(parseInt(data_value[2]), parseInt(data_value[3]), parseInt(data_value[4])),
            //     parseFloat(data_value[5])
            // ];
            var tmp = [
                Date.UTC(2010, parseInt(data_value[3]), parseInt(data_value[4])),
                parseFloat(data_value[5])
            ];

            ts_select_data.push(tmp);
            ts_select_name = data_value[2] + '-' + data_value[1];
            ts_select_subtitle = data_value[0] + ', ';
            // tmp = '';
        }

        // alert('ts_select_subtitle: '+ts_select_subtitle);

        // alert('NAME: '+ts_select_name);
        ts_subtitle = ts_subtitle + ts_select_subtitle;
        ts_select_subtitle = '';
        var ts_tmp_dict = {
            'name': ts_select_name,
            'data': ts_select_data
        }

        ts_series.push(ts_tmp_dict);

        // alert('ts_subtitle: '+ts_subtitle);
    }

    ts_subtitle = ts_subtitle.split(', ').filter(function (e, i, arr) {
                return arr.lastIndexOf(e) === i;
            }).join(', ');
    ts_subtitle = 'AOI: ' + ts_subtitle.substring(0, ts_subtitle.length - 2);

    initHighcharts(ts_series);

    // alert('SERIES SIZE: '+ts_series.length);
    // alert('NAME 0: '+ts_series[0]['name']);
    // alert('DATA 0: '+ts_series[0]['data']);

    // alert('NAME 1: '+ts_series[1]['name']);
    // alert('DATA 1: '+ts_series[1]['data']);

    // alert('NAME 2: '+ts_series[2]['name']);
    // alert('DATA 2: '+ts_series[2]['data']);
}

function initHighcharts(ts_series) {
    Highcharts.chart('container', {
        chart: {
            type: 'spline'
        },
        title: {
            text: title
        },
        subtitle: {
            text: ts_subtitle
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                month: '%e/%b'
            },
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: ts_units
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
        pointInterval: 24 * 3600 * 1000 // one day
    });
}


$(document).ready(function(){
    getDataSeries();
});
