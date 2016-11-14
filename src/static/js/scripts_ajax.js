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
                    data = 'To delete, select Item or more Itemss.';
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

// function initWikiUpdate(){
//     $('button.btn-link').click(function(event){
//         alert('initWikiUpdate');
//         var link = $(this);
//         var modal = $('#modalWiki');
//         var form_url = $('.form-modal').attr('action');
//         var wiki_id = link.attr("value")
//
//         // alert('link = '+link.attr("value"));
//
//         $.ajax({
//             'url': form_url,
//             'dataType': 'text',
//             'type': 'post',
//             data: {
//                 'wiki_id': wiki_id,
//                 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
//             },
//             'success': function(data, status, xhr){
//                 alert('status = '+status);
//
//                 var titleWiki = document.getElementById('title');
//
//                 alert('titleWiki = '+titleWiki.value);
//                 // check if we got successfull response from the server
//                 // if (status != 'success') {
//                 //   alert(gettext('There was an error on the server. Please, try again a bit later.'));
//                 //   return false;
//                 // }
//
//                 // update modal window with arrived content from the server
//                 // var modal = $('#modalWiki'),
//                 //   html = $(data), form = html.find('#content-column form');
//                 // modal.find('.modal-title').html(html.find('#content-column h2').text());
//                 // modal.find('.modal-body').html(form);
//
//                 // init our edit form
//                 // initEditWikiForm(form, modal);
//
//
//                 // setup and show modal window finally
//                 modal.modal({
//                     'keyboard': false,
//                     'backdrop': false,
//                     'show': true
//                 });
//             },
//             'error': function(){
//                 var message = 'An unexpected error occurred. Try later.';
//                 modal.find('.modal-body').html(message);
//                 modal.modal('show');
//                 // return false;
//             }
//         });
//
//         // var modal = $('#modalWiki');
//         // modal.modal('show');
//
//         return false;
//     });
// }

function initWikiUpdate() {
    $('a.wiki-edit-form-link').click(function(event){
        var link = $(this);
        $.ajax({
            'url': link.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'success': function(data, status, xhr){
                // check if we got successfull response from the server
                if (status != 'success') {
                    alert(gettext('There was an error on the server. Please, try again a bit later.'));
                    return false;
                }

                // update modal window with arrived content from the server
                var modal = $('#modalWiki'), html = $(data), form = html.find('#content-column form');
                modal.find('.modal-title').html(html.find('#content-column h2').text());
                modal.find('.modal-body').html(form);

                // init our edit form
                initEditWikiForm(form, modal);

                // setup and show modal window finally
                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true
                });
            },
            'error': function(){
                alert(gettext('There was an error on the server. Please, try again a bit later.'));
                return false
            }
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
            alert(gettext('There was an error on the server. Please, try again a bit later.'));
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
                setTimeout(function(){location.reload(true);}, 100);
            }
        }
    });
}


$(document).ready(function(){
    initCheckDeleteItems();
    initCheckCurDeleteItems();
    initPrelod();
    initWikiUpdate();
});
