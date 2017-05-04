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
                alert('ERROR: '+error);
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
                data_list = data.split('$$$')
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
        },
        'success': function(data, status, xhr){
            if (obj != datasets_id) {
                // setTimeout(function(){location.reload(true);}, 500);
                window.location.href = form_url;
            }
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

function setPolygon(obj) {
    // alert(obj.checked);
    var checked = obj.checked;
    var form_url = $('#customer_section').attr('action');
    
    if (checked) {
        $.ajax({
            url: form_url,
            type: 'GET',
            'async': true,
            'dataType': 'text',
            data: {
                'polygon': obj.value,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error){
                // alert('status 1: '+status);
                // alert('error: '+error);
                var message = 'An unexpected error occurred. Try later.';
            },
            'success': function(data, status, xhr){
                // alert('DATA: '+data);
                // var data_status = JSON.parse(data);
                // alert('URL: '+data_status.url);
                // alert('status: '+data_status.status);
                // if (data_status.status == 'reload') {
                //     window.location.href = form_url;
                // }
                // var uri_kml = data_status.url;
                // window.location.href = form_url;
                
                // alert('DATA: '+data);
                // var kml;
                // kml = new google.maps.KmlLayer(data);
                var kml = new google.maps.KmlLayer({url: data, map: map});
                // kml = new google.maps.KmlLayer('http://indy4.epcc.ed.ac.uk/media/kml/LinearRing.kml');
                // kml.setMap(map);
            },
        });
        return false;
    }
}

function sendDataToServer(obj) {
    // alert('sendDataToServer');
    // var send_data = JSON.parse(obj);
    // var send_data = JSON.parse(data);
    var form_url = $('#customer_section').attr('action');
    var obj_list = []
    var count = 0;
    var modal = $('#modalWaiting');
    modal.modal('show');
    
    for(n in obj) {
        var temp = [];
        var reverce_list = [];
        for(k in obj[n]) {
            temp.push(obj[n][k]);
            var reverce_list = temp.reverse();
        }
        // alert('reverce_list: '+reverce_list);
        obj_list.push(reverce_list);
    }
    
    $.ajax({
        url: form_url,
        type: 'POST',
        'async': true,
        'dataType': 'text',
        data: {
            'send_data': obj_list,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'error': function(xhr, status, error){
            // alert('error: '+error);
            var message = 'An unexpected error occurred. Try later.';
            alert(message);
        },
        'success': function(data, status, xhr){
            // alert('URL DATA: '+data);
            var obj_status = status;
            sendGetToServer();
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
                $('#areaName').val(data);
                modal.modal('show');
            },
        });
        return false;
    });
}

function deleteFile(ds) {
    
    var form_url = $('#customer_section').attr('action');
    var x = new XMLHttpRequest();
    x.open("GET", "/customer/delete?delete_file=del", true);
    x.send(null);
    
    // alert('DATA !!! '+form_url);
    
    $.ajax({
        url: '/customer/delete',
        type: 'GET',
        'async': true,
        'dataType': 'text',
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
            // alert('deleteTMPFile: '+data);
            // /media/temp_files/result.csv
            var obj_status = status;
            getTmpCSV(data);
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
