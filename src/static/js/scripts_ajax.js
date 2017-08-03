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
function myFunction(x, y, text, obj_id) {
    // console.log("MyFunction: x=" + x + ", y=" + y);
    var popup = document.getElementById(obj_id);
    popup.innerHTML = text;
    popup.style.left = x + "px";
    popup.style.top = y + "px";
    popup.style.visibility = "visible";
}

function createDiv(obj_id) {
    var divNode = document.createElement("div");
    divNode.setAttribute("class", "popup");
    divNode.setAttribute("id", obj_id);
    divNode.setAttribute("draggable", "true");

    divNode.innerHTML = 'A <b>different</b> Popup!<br> with multiple lines</span>';
    document.body.appendChild(divNode);
}

function drag_start(event) {
    var style = window.getComputedStyle(event.target, null);
    event.dataTransfer.setData("text/plain",
    (parseInt(style.getPropertyValue("left"), 10) - event.clientX) + ',' + (parseInt(style.getPropertyValue("top"),10) - event.clientY));
}

function drag_over(event) { 
    event.preventDefault(); 
    return false; 
}

function drop(event, obj_id) {
    alert('EVENT: '+event);
    alert('OBJ ID: '+$(this).attr("id"));
    
    $('.popup').live('click', function() {
         alert($(this).attr("id"));
    });
        

    var offset = event.dataTransfer.getData("text/plain").split(',');
    var dm = document.getElementById(obj_id);
    // console.log("drop: x="+parseInt(offset[0], 10)+", y="+parseInt(offset[1],10));
    dm.style.left = (event.clientX + parseInt(offset[0], 10)) + 'px';
    dm.style.top = (event.clientY + parseInt(offset[1], 10)) + 'px';
    event.preventDefault();
    return false;
}


function setPolygon(obj) {
    // alert(obj.checked);
    var checked = obj.checked;
    var form_url = $('#customer_section').attr('action');
    var polygon_name = obj.value;

    if (checked) {
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
            },
            'success': function(data, status, xhr){
                // alert('DATA: '+data);
                
                // When the user clicks on div, open the popup
                

                var kml = new google.maps.KmlLayer({
                    url: data,
                    suppressInfoWindows: true,
                    map: map
                });

                kml.addListener('click', function(kmlEvent) {
                    // alert('KML Click addListener! '+data);
                    // var text = kmlEvent.featureData.description;
                    // showInContentWindow(text);
                    
                    var centerX = document.documentElement.clientWidth / 2;
                    var centerY = document.documentElement.clientHeight / 2;

                    // alert('COORD X: '+centerX);
                    // alert('COORD Y: '+centerY);

                    createDiv(polygon_name);

                    var dm = document.getElementById(polygon_name);
                    dm.innerHTML = data;
                    dm.addEventListener('dragstart', drag_start, false); 
                    document.body.addEventListener('dragover', drag_over, false); 
                    document.body.addEventListener('drop', function() {drop(polygon_name)}, false);

                    // var dm = document.getElementById('myPopup');
                    // dm.innerHTML = data;
                    // dm.addEventListener('dragstart', drag_start, false); 
                    // document.body.addEventListener('dragover', drag_over, false); 
                    // document.body.addEventListener('drop', drop, false);

                    myFunction(centerX, centerY, data, polygon_name);
                });


                // kml.setMap(map);
            },
        });
        return false;
    }
}

function sendDataToServer(coord, reports, stats) {
    // alert('sendDataToServer REP: '+reports);
    // alert('sendDataToServer STAT: '+stats);

    var form_url = $('#customer_section').attr('action');
    var coord_list = []
    var count = 0;
    var modal = $('#modalWaiting');
    modal.modal('show');

    for(n in coord) {
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
        'success': function(data, status, xhr){
            // var message = JSON.parse(data);
            // var message = data['message'];

            // alert('sendDataToServer: '+data);

            // var obj_status = status;

            // sendGetToServer();
            setTimeout(sendGetToServer, 1000);
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
            
            // setTimeout(getTmpCSV, 100, data_aoi, stat);
            getPolygon(data_aoi, stat);
        },
    });
}

function sendDataAttrStatToServer(obj) {
    var form_url = $('#customer_section').attr('action');
    var attr_list = [];
    var stat_list = [];

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

    $.ajax({
        url: form_url,
        type: 'POST',
        'async': true,
        'dataType': 'text',
        data: {
            'button': $(obj).val(),
            'attr_list': attr_list,
            'stat_list': stat_list,
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

            // function reload() {
            //     alert('URL DATA: '+data);
            //     window.location.href = form_url;
            // }
            //
            // setTimeout(reload, 100);

            window.location.href = form_url;


            // $("#ds_show span").text('new_data[0]');
            // $("#ds_show span").text(new_data[0]);
            // $("span#img_show").text(new_data[1]);
            // $("span#stat_show").text(new_data[2]);
            //
            // alert('URL DATA: '+data);
            // sendGetToServer();
            // window.location.href = form_url;


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

function movingInfoWindow() {
    $('.gm-style-iw').click(function(){
        alert('Вы нажали на элемент "foo"');
    });
}

// 
// 


// function clickUpdate() {
//     var values = [];
//     var modal = $('#modalUpdate');
//     var form_modal = $('.form-modal').attr('action');
//     modal.modal('show');

//     $.ajax({
//         url: form_modal,
//         type: 'GET',
//         'async': true,
//         'dataType': 'text',
//         data: {
//             'update': 'update',
//             'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
//         },
//         'error': function(xhr, status, error){
//             var message = 'An unexpected error occurred. Try later.';
//             modal.find('.modal-body').html(message);
//             modal.modal('show');
//         },
//         'success': function(data, status, xhr){
//             setTimeout(modal.modal('hide'), 3000);
//         },
//     });
// }


$(document).ready(function(){
    initCheckDeleteItems();
    initCheckCurDeleteItems();
    initPrelod();
    initUploadFile();
    initAddOverrideMaping();
    initEditArea();
    // deleteFile();
});
