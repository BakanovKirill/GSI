function getFileName() {
    $('input[type="file"]').on('change', function (event, files, label) {
        var file_name = document.getElementById('id_test_data').files[0].name;
        $('span.file-selected').text(file_name);

        if (file_name != 'No file selected.') {
            $('#load').removeAttr('disabled');
        } else if (file_name == 'No file selected.') {
            $('#load').attr('disabled','disable');
        }
        // alert('FILE 2: '+file_name);
    });
}

function selectedAttribute() {
    var list_attr = '';
    var select_statistic = $('#select_statistic').val();
    var select_attr = $('#select_attr').val();

    console.log('ATTR: ', select_attr);
    console.log('STAT: ', select_statistic);

    if (select_statistic && select_attr) {
        $('#calculate_data').removeAttr('disabled');
    } else {
        $('#calculate_data').attr('disabled','disable');
    }

    if ($('#select_attr').val()) {
        console.log('YES');
        list_attr = $('#select_attr').val();
        var start_title = '';

        for (var m = 0; m < list_attr.length; m++) {
            console.log('list_attr: ', list_attr[m]);

            var aoi_tmp = list_attr[m].split('_');
            start_title += aoi_tmp[0] + ', ';
        }

        console.log('start_title: ', start_title);

        start_title = start_title.substring(0, start_title.length - 1);
        start_title = start_title.substring(0, start_title.length - 1);

        console.log('start_title: ', start_title);
    } else {
        console.log('NO');
        var start_title = 'None';
    }

    console.log('start_title: ', start_title);

    $('#attr_selected span').text(start_title);

    console.log('selectedAttribute select_attr: ', start_title);
}

function selectedStatistic() {
    var select_statistic = $('#select_statistic').val();
    var select_attr = $('#select_attr').val();

    console.log('ATTR: ', select_attr);
    console.log('STAT: ', select_statistic);

    if (select_statistic && select_attr) {
        $('#calculate_data').removeAttr('disabled');
    } else {
        $('#calculate_data').attr('disabled','disable');
    }

    $('#stat_selected span').text(select_statistic);
    console.log('selectedStatistic select_statistic: ', select_statistic);
}

function setStatistic() {
    var select_statistic = $('#select_statistic').val();
    var select_attr = $('#select_attr').val();

    console.log('ATTR: ', select_attr);
    console.log('STAT: ', select_statistic);

    if (select_statistic && select_attr) {
        $('#calculate_data').removeAttr('disabled');
    } else {
        $('#calculate_data').attr('disabled','disable');
    }

    $('#stat_selected span').text(select_statistic);
    console.log('selectedStatistic select_statistic: ', select_statistic);
}

// function startModalWait() {
//     var modal = $('#modalWaiting');
//     modal.modal('show');
// }

function go_progress_ts(progress_bar, ts_section) {
    console.log('showWaiting COUNT TS: '+count_ts);
    
    console.log('1 GO progress TS: ', progress_bar);
    console.log('1 GO time_section: ', ts_section);

    progress = progress_bar;
    time_section = ts_section;

    progress = parseFloat((progress + time_section).toFixed(1));

    // console.log('11 GO progress TS: ', progress);
    // console.log('11 GO time_section: ', time_section);

    if (progress < 100) {
        document.getElementById('progress_bar').innerHTML = progress + ' %';
        document.getElementById('progress_bar').style.width = progress + '%';
        
        // console.log('< 100 GO progress TS: ', progress);
    }
    else {
        document.getElementById('progress_bar').innerHTML = '100 %';
        document.getElementById('progress_bar').style.width = 100 + '%';

        // console.log('> 100 GO progress TS: ', progress);

        // stopTimeout();

        clearInterval(timerId);
        progress = 0;
        time_section = 0;
    }

    // console.log('2 GO progress TS: ', progress);
    // console.log('2 GO time_section: ', time_section);
}

function setToZero() {
    document.getElementById('progress_bar').innerHTML = '0 %';
    document.getElementById('progress_bar').style.width = 0 + '%';
}

function showWaitingCalculation() {
    count_ts = parseInt(count_ts)
    console.log('showWaiting COUNT TS: '+count_ts);
    // debugger;
    // console.time('test');

    // clearInterval(timerId);
    // progress = 0;
    // time_section = 0;
    var modal_calc = $('#modalCalculationAoi');
    var modal = $('#modalWaiting');
    // var modal = document.getElementById('modalWaiting_1');
    modal_calc.modal('hide');
    modal.modal('show');

    if (count_ts) {
        // var count_timeseries = count_ts * 5;
        var time_interval = 400;
        time_section = parseFloat((100 / count_ts).toFixed(1));
        setToZero();
    } else {
        var time_interval = 60;
        time_section = parseInt(100 / count_rep);
        setToZero();
    }

    // console.log('progress START: ', progress);
    // console.log('time_section: ', time_section);

    timerId = setInterval(function() {
        go_progress_ts(progress, time_section);
    }, time_interval);

    // console.timeEnd('showWaiting: ', count_ts);
}


$(document).ready(function(){
    getFileName();
    setStatistic();
});
