function getDataSeries() {
    // alert('getDataSeries: '+select_diagram);
    // alert('ts_subtitle: '+ts_subtitle);
    
    if (ts_data) {
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
                ts_select_name = data_value[2] + '-' + data_value[1] + '-' + data_value[0];
                ts_select_subtitle = data_value[0] + ', ';
                // tmp = '';
                
                // alert('ts_select_name: '+ts_select_name);
                // alert('ts_select_data: '+ts_select_data);
            }

            // alert('NAME: '+ts_select_name);
            // alert('ts_select_data: '+ts_select_data);

            // alert('ts_select_subtitle: '+ts_select_subtitle);

            
            ts_subtitle = ts_subtitle + ts_select_subtitle;
            ts_select_subtitle = '';
            var ts_tmp_dict = {
                'name': ts_select_name,
                'data': ts_select_data
            }

            ts_series.push(ts_tmp_dict);

            // alert('ts_series: '+ts_series);
        }

        ts_subtitle = ts_subtitle.split(', ').filter(function (e, i, arr) {
                    return arr.lastIndexOf(e) === i;
                }).join(', ');
        ts_subtitle = 'AOI: ' + ts_subtitle.substring(0, ts_subtitle.length - 2);

        if (select_diagram == 'line') {
            initHighchartsLine(ts_series);
        } else if (select_diagram == 'box') {
            // alert('BOX');
            initHighchartsBox();
        }
        

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
    Highcharts.chart('container', {
        chart: {
            type: 'spline'
        },
        title: {
            text: ''
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

function initHighchartsBox() {
    Highcharts.chart('container', {

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
            categories: ['1/06', '2', '3', '4', '5', '6'],
            title: {
                text: 'Date'
            }
        },

        yAxis: {
            title: {
                text: 'Observations'
            },
            plotLines: [{
                value: 932,
                color: 'red',
                width: 1,
                label: {
                    text: 'Theoretical mean: 932',
                    align: 'center',
                    style: {
                        color: 'gray'
                    }
                }
            }]
        },

        series: [{
            name: 'Observations',
            data: [
                [760, 801, 848, 795, 1000],
                [733, 853, 939, 780, 1100],
                [714, 762, 817, 770, 1050],
                [724, 802, 806, 771, 1535],
                [834, 836, 864, 782, 1005],
                [834, 836, 864, 782, 1005],
                [834, 836, 864, 782, 1005],
                [834, 836, 864, 782, 1005]
            ],
            tooltip: {
                headerFormat: '<em>Experiment No {point.key}</em><br/>'
            }
        }, {
            name: 'Outlier',
            color: Highcharts.getOptions().colors[0],
            type: 'scatter',
            data: [ // x, y positions where 0 is the first category
                [0, 644],
                [2, 718],
                [4, 951],
                [4, 969],
                [4, 1000]
            ],
            marker: {
                fillColor: 'white',
                lineWidth: 1,
                lineColor: Highcharts.getOptions().colors[0]
            },
            tooltip: {
                pointFormat: 'Observation: {point.y}'
            }
        }]
    });
}


$(document).ready(function(){
    getDataSeries();
});
