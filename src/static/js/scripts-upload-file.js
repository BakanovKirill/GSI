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


$(document).ready(function(){
    getFileName();
    setStatistic();
});
