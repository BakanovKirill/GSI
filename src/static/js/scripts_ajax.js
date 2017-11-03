// var progress = 0;
// var interval_id;
// var time_section = 0;
var is_visible_aoi = false;

function initCheckDeleteItems() {
    $('button.check-delete').click(function(event){
        var values = [];
        var modal = $('#modalCheckDelete');
        var form_modal = $('.form-modal').attr('action');

        $(':checkbox:checked').each(function(){
            values.push(this.value);
        });

        $.ajax({
            url: form_modal,
            type: 'POST',
            'async': true,
            'dataType': 'text',
            data: {
                'run_id': values,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                var message = 'An unexpected error occurred. Try later.';
                modal.find('.modal-body').html(message);
                modal.modal('show');

            },
            'success': function(data, status, xhr){
                if (!data){
                    data = 'To delete, select Item or more Items.';
                    modal.find('div.div-cancel').removeClass("col-sm-6");
                    modal.find('div.div-cancel').addClass("col-sm-4 col-sm-offset-4")
                    modal.find('.cancel-but').html('Ok');
                    modal.find('.del-but').hide();
                }
                else {
                    modal.find('.cancel-but').html("No. I don't want delete this Item.");
                    modal.find('div.div-cancel').removeClass("col-sm-4 col-sm-offset-4");
                    modal.find('div.div-cancel').addClass("col-sm-6");
                    modal.find('.del-but').show();
                }
                modal.find('.modal-body').html(data);
                modal.modal('show');
            },
        });
        return false;
    });
}

function initCheckCurDeleteItems() {
    $('button.check-cur-delete').click(function(event){
        var modal = $('#modalCheckDelete');
        var form_modal = $('.form-modal').attr('action');
        var cur_delete = $(this).val();

        // alert('cur_delete: '+cur_delete);

        $.ajax({
            url: form_modal,
            type: 'POST',
            'async': true,
            'dataType': 'text',
            data: {
                'cur_run_id': cur_delete,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                // alert('ERROR: '+error);
                var message = 'An unexpected error occurred. Try later.';
                modal.find('.modal-body').html(message);
                modal.modal('show');
            },
            'success': function(data, status, xhr){
                modal.find('.cancel-but').html("No. I don't want delete this item.");
                modal.find('div.div-cancel').removeClass("col-sm-4 col-sm-offset-4");
                modal.find('div.div-cancel').addClass("col-sm-6");
                modal.find('.del-but').show();
                modal.find('.modal-body').html(data);
                modal.find('.del-but').val(cur_delete);
                modal.modal('show');
            },
        });
        return false;
    });
}

function initPrelod(){
    $('button.pre-process').click(function(event){
        var modal = $('#modalPreload');
        var form_url = $('.form-modal').attr('action');
        var cur_run_id = $('input:radio[name=execute_runs]:checked').val();

        $.ajax({
            url: form_url,
            type: 'POST',
            'async': true,
            'dataType': 'text',
            data: {
                'cur_run_id': cur_run_id,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                var message = 'An unexpected error occurred. Try later.';
                $('<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>').prependTo("div.modal-header");
                modal.find('.modal-body').html(message);
                modal.modal('show');
                $('.modal-content').click(function(){
                    // location.reload(True);
                    $(location).attr('href',form_url);
                });

            },
            beforeSend: function(){
                // alert('beforeSend');
                $(".close").remove();
                modal.find('div.progress').removeClass("disabled");
                modal.find('div.progress').addClass("visible");
                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true
                });
	        },
            'success': function(data, status, xhr){
                // alert(data);
                $("#modalfooter").remove();
                $('<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>').prependTo("div.modal-header");

                if (data !== 'For start choose Run') {
                    // alert('For start choose Run');
                    modal.find('.modal-body').html(data);
                    // setTimeout(function() {$(location).attr('href',form_url);}, 3000);
                } else {
                    // alert('NO For start choose Run');
                    modal.find('.modal-body').html(data);
                }

                $('.modal-content').click(function(){
                    // alert('CLICK');
                    // location.reload(True);
                    $(location).attr('href',form_url);
                });
            },
        });
        return false;
    });
}

function initEditWikiForm(form, modal) {
    // close modal window on Cancel button click
    form.find('input[name="cancel_button"]').click(function(event){
        modal.modal('hide');
        return false;
    });

    // make form work in AJAX mode
    form.ajaxForm({
        'dataType': 'html',
        'error': function(){
            alert('There was an error on the server. Please, try again a bit later.');
            return false;
        },
        'success': function(data, status, xhr) {
            var html = $(data), newform = html.find('#content-column form');

            // copy alert to modal window
            modal.find('.modal-body').html(html.find('.alert'));

            // copy form to modal if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);

                // initialize form fields and buttons
                initEditWikiForm(newform, modal);
            } else {
                // if no form, it means success and we need to reload page
                // to get updated wiki article;
                // reload after 2 seconds, so that user can read success message
                setTimeout(function(){location.reload(true);}, 50);
            }
        }
    });
}

function initUploadFile(){
    $('#btnPicture').click(function(event){
        var values = [];
        var modal = $('#uploadFile');
        var form_modal = $('.form-modal').attr('action');

		modal.modal('show');
    });
}

function initAddOverrideMaping() {
    $('#add_override_maping_button').click(function(event){
        var shelf_data_id = $('input[name="shelf_data_select"]:checked').val();
        var form_url = $('#static_data').attr('action');

        $.ajax({
            url: form_url,
            type: 'POST',
            'async': true,
            'dataType': 'text',
            data: {
                'shelf_data_id': shelf_data_id,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                var message = 'An unexpected error occurred. Try later.';
            },
            'success': function(data, status, xhr){
                var data_list = data.split('$$$')
                var root_filename = $('#id_root_filename');
                var attribute_name = $('#id_attribute_name');

                // alert('DATA 1: '+data_list[0]);
                // alert('DATA 2: '+data_list[1]);

                $(root_filename).val(data_list[0]);
                $(attribute_name).val(data_list[1]);
            },
        });
        return false;
    });
}

function getCheckboxValues() {
    var list = null;
    list = $('.checkboxes_root_filenames :checkbox:checked');

    // alert(list.length);

	return list;
}

function showDataSets(obj) {
    var select_dataset = $("#mydataset option:selected");
    var datasets_id = $(select_dataset).val();
    var form_url = $('#customer_section').attr('action');

    var modal = $('#modalWaitingNormal');
    modal.modal('show');

    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'datasets_id': datasets_id,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('status 1: '+status);
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('success: '+data);
            // alert('success status: '+status);
            window.location.href = form_url;

            // if (obj != datasets_id) {
            //     // setTimeout(function(){location.reload(true);}, 500);
            //     window.location.href = form_url;
            // }
        },
    });
    return false;
}

function showFileSelectArea(elem) {
    var select_area = $("#show_file_arrea option:selected");
    var show_file_arrea = $(select_area).val();
    var form_url = $('#customer_section').attr('action');

    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'show_file_arrea': show_file_arrea,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            if (elem != show_file_arrea && show_file_arrea != 'none_file') {
                // setTimeout(function(){location.reload(true);}, 500);
                window.location.href = form_url;
            }
        },
    });
    return false;
}

function removeSelectedItems() {
    // var select_dataset = $("#mydataset option:selected");
    // var datasets_id = $(select_dataset).val();
    var form_url = $('#customer_section').attr('action');

    // alert('obj: '+obj);
    // alert('datasets_id: '+datasets_id);
    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'remove_all_selected_items': 'remove_all_selected_items',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('status 1: '+status);
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
        },
        'success': function(data, status, xhr){
            window.location.href = form_url;
        },
    });
    return false;
}

// For create movable info windows
var div_id;
var close_window_id;

function mOver(obj) {
    div_id = obj.id;
}

// <span class="close" id="close">&times;</span>

function createDiv(obj_id, msg) {
    // var spanNode = document.createElement("span");
    // spanNode.setAttribute("class", "close");
    // spanNode.setAttribute("id", "close");
    // spanNode.innerHTML = '&times;';

    // var insert_text = msg + '<span class="close" id="close">&times;</span>';

    var divNode = document.createElement("div");
    divNode.setAttribute("class", "popup");
    divNode.setAttribute("id", obj_id);
    divNode.setAttribute("draggable", "true");
    divNode.setAttribute("onmouseover", "mOver(this)");
    // divNode.setAttribute("ondrop", "drop(event)");
    // 
    // alert('TEXT: '+insert_text);

    // divNode.innerHTML = msg;
    
    // divNode.appendChild(spanNode);
    // document.body.appendChild(spanNode);
    document.body.appendChild(divNode);
    // document.body.appendChild(spanNode);
    // 
    // divNode.appendChild(spanNode);
}


// When the user clicks on div, open the popup
function myFunction(x, y, text, div_id) {
    // console.log("MyFunction: x="+x+", y="+y);
    var popup = document.getElementById(div_id);
//    var canvas = document.getElementById('canvas1');
//    var rect = canvas.getBoundingClientRect();
//    popup.style.left=x+rect.left+"px";
//    popup.style.top=y+rect.top+"px";
    popup.innerHTML = text;
    popup.style.left = x + "px";
    popup.style.top = y + "px";
    popup.style.visibility = "visible";
}

function drag_start(event) {
    var style = window.getComputedStyle(event.target, null);
    event.dataTransfer.setData("text/plain",
    (parseInt(style.getPropertyValue("left"), 10) - event.clientX) + ',' + (parseInt(style.getPropertyValue("top"), 10) - event.clientY));
}

function drag_over(event) { 
    event.preventDefault(); 
    return false; 
}

function drop(event) {
    // alert('CLOSE ID: '+close_window_id);
    // alert('EVENT DROP 1: '+event.target.id);
    // feat_4_iw

    var dm = document.getElementById(div_id);
    // var dm = document.getElementById('feat_4_iw');
    var offset = event.dataTransfer.getData("text/plain").split(',');
    
    // console.log("drop: x="+parseInt(offset[0], 10)+", y="+parseInt(offset[1], 10));
    dm.style.left = (event.clientX + parseInt(offset[0], 10)) + 'px';
    dm.style.top = (event.clientY + parseInt(offset[1], 10)) + 'px';
    event.preventDefault();

    return false;
}

function closeIF() {
    // alert('closeIF');
    var div_info = document.getElementById(div_id);
    div_info.parentNode.removeChild(div_info);
}


function setPolygon(obj) {
    // alert('CHECKED: '+obj.checked);

    var checked = obj.checked;
    var form_url = $('#customer_section').attr('action');
    var polygon_name = obj.value;

    // alert('AOI NAME: '+polygon_name);

    if (checked) {
        // alert('CHECKED: '+checked);
        $.ajax({
            url: form_url,
            type: 'GET',
            'async': true,
            'dataType': 'text',
            data: {
                'polygon': polygon_name,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                // alert('status 1: '+status);
                // alert('error: '+error);
                var message = 'An unexpected error occurred. Try later.';
                alert(message);
            },
            'success': function(data, status, xhr){
                // alert('DATA: '+data);
                var data_list = data.split('$$$');

                // alert('DATA 0: '+data_list[0]);
                // alert('DATA 1: '+data_list[1]);
                // alert('DATA 2: '+data_list[2]);
                
                console.log('DATA 1: ', data_list[1]);

                // alert('DATA URL: '+data_list[0]);
                // alert('DATA ID: '+data_list[2]);
                
                // When the user clicks on div, open the popup
                

                
                if (data_list[1] == 'false') {
                    kml = new google.maps.KmlLayer({
                        url: data_list[0],
                        // suppressInfoWindows: true,
                        suppressInfoWindows: false,
                        map: map
                    });
                } else {
                    kml = new google.maps.KmlLayer({
                        url: data_list[0],
                        suppressInfoWindows: true,
                        // suppressInfoWindows: false,
                        map: map
                    });
                }
                
                console.log('URL: ', data_list[0]);
                // console.log('DATA LIST 11: ', data_list[1]);

                // alert('URL: '+data_list[1]);

                kml.addListener('click', function(kmlEvent) {
                    // alert("KML DATA: "+data);
                    
                    var msg = data_list[1];
                    // var info_window_id = kmlEvent.featureData.name;
                    var info_window_id = polygon_name;
                    close_window_id = data_list[2];

                    // console.log("KML DATA: "+data);
                    // console.log("KML MSG: "+msg);
                    console.log("KML ID: "+info_window_id);

                    if (data_list[1] != 'false') {
                        createDiv(info_window_id, msg);

                        var centerX = document.documentElement.clientWidth / 2;
                        var centerY = document.documentElement.clientHeight / 2;

                        var dm = document.getElementById(info_window_id);
                        dm.addEventListener('dragstart', drag_start, false); 
                        document.body.addEventListener('dragover', drag_over, false); 
                        document.body.addEventListener('drop', drop, false);
                        
                        myFunction(centerX, centerY, msg, info_window_id);
                    }
                    

                    // alert("KML ID: "+info_window_id);
                    // alert("KML featureData: "+kmlEvent.featureData);
                    // alert("KML NAME: "+kmlEvent.featureData.name);
                    

                    // ***********************************************************************************

                    // var divNode = document.createElement("div");
                    // divNode.setAttribute("class", "popup");
                    // divNode.setAttribute("id", "myPopup");
                    // divNode.setAttribute("draggable", "true");
                    // divNode.innerHTML = 'A <b>different</b> Popup!<br> with multiple lines</span>';
                    // document.body.appendChild(divNode);

                    // var dm = document.getElementById('myPopup'); 
                    // dm.addEventListener('dragstart',drag_start,false); 
                    // document.body.addEventListener('dragover',drag_over,false); 
                    // document.body.addEventListener('drop',drop,false);
                    // 
                    // ***********************************************************************************
                    
                    

                    // // alert('COORD X: '+centerX);
                    // // alert('COORD Y: '+centerY);
                    
                    // alert('EVENT addListener ID: '+info_window_id);

                    // createDiv(info_window_id);
                    // 
                    // 

                    // var dm = document.getElementById(info_window_id);
                    // // dm.innerHTML = data;
                    // dm.addEventListener('dragstart', drag_start, false); 
                    // document.body.addEventListener('dragover', drag_over, false); 
                    // document.body.addEventListener('drop', drop, false);
                    

                    // // document.body.addEventListener('click', close, false);

                    // // myFunction(centerX, centerY, data, info_window_id);
                    // // var insert_text = msg + '<span class="close" id="close">&times;</span>';
                    // myFunction(centerX, centerY, msg, info_window_id);
                    // // myFunction(centerX, centerY, data);
                });

                kml.setMap(map);
                kml_arr[polygon_name] = kml;

                // console.log('KML ARR: ', kml_arr);
            },
        });

        return false;
    } else {
        // var info_window_id = kmlEvent.featureData.name;

        // alert('KML ID: '+info_window_id);

        obj_kml = kml_arr[polygon_name];
        obj_kml.setMap(null);

        var infor_window_aoi = document.getElementById(polygon_name);

        if (infor_window_aoi) {
            infor_window_aoi.remove();
        }
        

        return false;
    }
}

function go_progress() {
    // alert('GO progress: '+progress);
    // console.log('go_progress time_interval: ', time_interval);
    
    // progress += time_section;
    progress = parseFloat((progress + time_section).toFixed(1));

    // console.log('GO progress: ', progress);
    // console.log('GO time_section: ', time_section);

    if (progress < 100) {
        console.log('< 100 GO progress: ', progress);
        
        document.getElementById('progress_bar').innerHTML = progress + ' %';
        document.getElementById('progress_bar').style.width = progress + '%';
    } else {
        console.log('> 100 GO progress: ', progress);

        document.getElementById('progress_bar').innerHTML = '100 %';
        document.getElementById('progress_bar').style.width = 100 + ' %';

        clearInterval(timerId);
        progress = 0;
        time_section = 0;
    }
}

function sendDataToServer(coord, reports, stats) {
    // console.log('sendDataToServer REP: '+reports);
    // alert('sendDataToServer REP: '+reports);

    var form_url = $('#customer_section').attr('action');
    var coord_list = []
    // var count = 0;
    var modal = $('#modalWaiting');
    modal.modal('show');
    count_rep = reports.length

    if (count_rep <= 2) {
        var count_reports = count_rep * 10;
    }
    else {
        var count_reports = count_rep;
    }
    
    // var time_interval = 200 / count_reports;
    // var time_interval = parseFloat((100 / count_reports).toFixed(1));
    var time_interval = 60;


    time_section = parseInt(100 / count_reports);

    // alert('sendDataToServer REP: '+count_reports);
    // alert('sendDataToServer time_interval: '+time_interval);
    console.log('sendDataToServer count_reports: ', count_reports);
    console.log('sendDataToServer time_section: ', time_section);

    // timerId = setInterval(go_progress(), count_reports);

    timerId = setInterval(function() {
        go_progress();
    }, time_section);

    // console.log('sendDataToServer COUNT REP: '+count_reports);

    // alert('reports.length: '+reports.length);
    // alert('count_reports: '+count_reports);
    // alert('time_section: '+time_section);

    for (n in coord) {
        var temp = [];
        var reverce_list = [];
        for(k in coord[n]) {
            temp.push(coord[n][k]);
            var reverce_list = temp.reverse();
        }
        // alert('reverce_list: '+reverce_list);
        coord_list.push(reverce_list);
    }

    $.ajax({
        url: form_url,
        type: 'POST',
        'async': true,
        'dataType': 'text',
        data: {
            // 'send_data': coord_list,
            'coordinate_list': coord_list,
            'reports': reports,
            'stats': stats,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        beforeSend: function(){
            // alert('beforeSend');
            // interval_id = setInterval(go_progress, count_reports);
        },
        'success': function(data, status, xhr){
            // alert(data);
            // clearInterval(timerId);
            count_ts = data;
            // progress = 0;
            // time_section = 0;

            // console.log('success progress: ', progress);

            // var message = JSON.parse(data);
            // var message = data['message'];

            // alert('sendDataToServer: '+data);

            // var obj_status = status;
            
            // if (data = 'end') {
            //     sendGetToServer();
            // }

            sendGetToServer();
            
            // setTimeout(sendGetToServer, 1000);
        },
    });
}

function initEditArea() {
    $('button.edit-area').click(function(event){
        // alert('initEditArea');
        var modal = $('#modalEditArea');
        var form_modal = $('.form-modal').attr('action');
        var cur_area = $(this).val();

        // alert('cur_area: '+cur_area);

        $.ajax({
            url: form_modal,
            type: 'GET',
            'async': true,
            'dataType': 'text',
            data: {
                'cur_area': cur_area,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                // alert('ERROR: '+error);
                var message = 'An unexpected error occurred. Try later.';
                modal.find('.modal-body').html(message);
                modal.modal('show');
            },
            'success': function(data, status, xhr){
                // alert('DAATA: '+data);
                polygon = data.split('$')
                $('#areaName').val(polygon[0]);
                $('#save_area_name').val(polygon[1]);
                modal.modal('show');
            },
        });
        return false;
    });
}

function deleteFile(ds) {
    // alert('deleteFile '+ds);
    var form_url = $('#customer_section').attr('action');
    var x = new XMLHttpRequest();
    x.open("GET", "/customer/delete?delete_file=del", true);
    x.send(null);

    $.ajax({
        url: '/customer/delete',
        type: 'GET',
        'async': true,
        'dataType': 'json',
        data: {
            'delete_file': ds,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('DATA deleteTMPFile: '+data);
            // alert('deleteTMPFile status: '+status);
            // /media/temp_files/result.csv
            var obj_status = status;
            var data_aoi = data['data_aoi'];
            var stat = data['static'];
            var error = data['error'];

            if (error) {
                alert(error);
                var modal = $('#modalWaiting');
                modal.modal('hide');
            } else {
                getPolygon(data_aoi, stat);
            }
            
            // setTimeout(getTmpCSV, 100, data_aoi, stat);
            // getPolygon(data_aoi, stat);
        },
    });
}

function sendDataAttrStatToServer(obj) {
    var form_url = $('#customer_section').attr('action');
    var attr_list = [];
    var stat_list = [];
    var center_map = map.getCenter();

    // alert('BUT: '+$(obj).val());

    $('#view_attribute input:checkbox:checked').each(function(){
        // alert($(this).val());
        attr_list.push($(this).val())
    });

    $('#statictics_list input:radio:checked').each(function(){
        // alert($(this).val());
        stat_list.push($(this).val())
    });

    // alert('attr_list: '+attr_list);
    // alert('stat_list: '+stat_list);
    
    // alert('CENTER LAT: ' + center_map.lat());
    // alert('CENTER LNG: ' + center_map.lng());

    $.ajax({
        url: form_url,
        type: 'POST',
        'async': true,
        'dataType': 'text',
        data: {
            'button': $(obj).val(),
            'attr_list': attr_list,
            'stat_list': stat_list,
            'zoom_map': map.getZoom(),
            'center_lat': center_map.lat(),
            'center_lng': center_map.lng(),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('URL DATA: '+data);
            // var new_data = data.split('$');
            // setTimeout(reload, 100);

            window.location.href = form_url;
        },
    });
}

function sendDataTsToServer(obj) {
    var form_url = $('#customer_section').attr('action');
    var ts_list = [];
    var aoi_list = [];

    var select_diagram = $("#select_diagram").val();
    // var select_aoi = $("#select_aoi");
    var select_aoi = $('#select_aoi').val();
    var select_year = $('#select_year').val();
    var modal = $('#modalWaitingNormal');

    for (var m = 0; m < select_aoi.length; m++) {
        console.log('AOI: ', select_aoi[m]);

        var aoi_tmp = select_aoi[m].split('_');
        
        aoi_list.push(aoi_tmp[aoi_tmp.length-1]);

        // alert('AOIs: '+aoi_list);
        console.log('AOIs: ', aoi_list);
    }

    console.log('select_aoi: ', select_aoi);
    console.log('aoi_list: ', aoi_list);

    if ($(obj).val() === 'draw_plot') {
        modal.modal('show');
        // alert('button: '+$(obj).val());
    }

    
    // $('#select_aoi').on('show.bs.select', function (e) {
    //     alert('1: '+$(this).val());
    // });

    // $('#select_aoi').selectpicker('selectAll').each(function() {
    //     alert('2: '+$(this).val());
    // });

    console.log('YEAR: ', select_year);
    console.log('AOIs: ', aoi_list);

    $('#ts input:checkbox:checked').each(function(){
        // alert($(this).val());
        
        ts_list.push($(this).val())
    });

    // window.location.href = form_url;

    // alert('select_aoi: '+aoi_list);
    // alert('ts_list: '+ts_list);
    // alert('button: '+$(obj).val());

    $.ajax({
        url: form_url,
        type: 'POST',
        'async': true,
        'dataType': 'text',
        data: {
            'button': $(obj).val(),
            'ts_list': ts_list,
            'select_diagram': select_diagram,
            // 'select_aoi': select_aoi,
            'select_aoi': aoi_list,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('URL DATA: '+data);
            
            // setTimeout(reload, 100);

            

            // var modal = $('#modalWaitingNormal');
            // modal.modal('show');

            window.location.href = form_url;

            // if ($(obj).val() === 'draw_plot') {
                

                
            //     modal.modal('show');

            //     alert('button: '+$(obj).val());
            // }
        },
    });
}

function selectTab(obj) {
    var form_url = $('#customer_section').attr('action');
    var tab_name = $(obj).attr('value');

    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'tab_active': tab_name,
            // 'report_list': report_list,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('URL DATA: '+data);
            // sendGetToServer();
            
            if (data == 'ts' || tab_name == 'ts') {
                window.location.href = form_url;
                var modal = $('#modalWaitingNormal');
                modal.modal('show');
            }
        },
    });
}

function regenerateLegend() {
    // alert('regenerateLegend');
    // alert('Zoom: ' + zoom);
    var form_url = $('#customer_section').attr('action');

    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'regenerate_legend': 'regenerate_legend',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('URL DATA: '+data);
            // var obj_status = status;
            // sendGetToServer();
            window.location.href = form_url;
        },
    });
}

function resetSessionData() {
    // alert('regenerateLegend');
    // alert('Zoom: ' + zoom);
    var form_url = $('#reset_session').attr('action');

    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'reset_session': 'reset_session',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('URL DATA: '+data);
            // var obj_status = status;
            // sendGetToServer();
            window.location.href = form_url;
        },
    });
}

function getZoomGoogleMap(zoom) {
    // alert('Zoom IN: ' + zoom);
    var form_url = $('#customer_section').attr('action');

    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'zoom': zoom,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('URL DATA: '+data);
            // var obj_status = status;
            // sendGetToServer();
            // window.location.href = form_url;
        },
    });
}

function clearTs() {
    var form_url = $('#customer_section').attr('action');
    var modal = $('#modalWaitingNormal');
    modal.modal('show');

    $.ajax({
        url: form_url,
        type: 'GET',
        'async': true,
        'dataType': 'text',
        data: {
            'clear_ts': 'clear_ts',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            window.location.href = form_url;
            // alert('URL DATA: '+data);
            // var obj_status = status;
            // sendGetToServer();
            // window.location.href = form_url;
        },
    });
}



$(document).ready(function(){
    initCheckDeleteItems();
    initCheckCurDeleteItems();
    initPrelod();
    initUploadFile();
    initAddOverrideMaping();
    initEditArea();
    // deleteFile();
});
