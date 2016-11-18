function initUploadStaticData() {
  $('a#upload_file').click(function(event){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      //'type': 'post',
      'success': function(data, status, xhr){
        // check if we got successfull response from the server
        if (status != 'success') {
          alert('Error on the server. Please try again later.');
          return false;
        }

        // update modal window with arrived content from the server
        var modal = $('#modalUpload'),
          html = $(data), form = html.find('#header form');
        modal.find('.modal-title').html(html.find('#header h2').text());
        modal.find('.modal-body').html(form);

        // init our edit form
        initUploadStaticDataForm(form, modal);

        // setup and show modal window finally
        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'error': function(){
        alert('Error on the server. Please try again later.');
        return false
      }
    });

    return false;
  });
}

function initUploadStaticDataForm(form, modal) {
  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
  });

  // make form work in AJAX mode
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
        alert('Error on the server. Please try again later.');
        return false;
    },

    'beforeSend': function(xhr, settings){
        $("#load").prop("disabled", true);
        // $("#submit-id-cancel_button").prop("disabled", true);
        // $('.form-horizontal').html('<img id="loader-img" alt="" src="http://adrian-design.com/images/loading.gif" width="100" height="100" align="center" />', 3000);
        $('.form-horizontal').html('<img id="loader-img" alt="" src="" width="100" height="100" align="center" />', 3000);
      },
    'error': function(xhr, status, error){
        alert(error);
        // indicator.hide();
    },

    'success': function(data, status, xhr) {
        // alert('STOP');

      var html = $(data), newform = html.find('#content-column form');

      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      // copy form to modal if we found it in server response
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);

        // initialize form fields and buttons
        initCreateStudentForm(newform, modal);
      } else {
        // if no form, it means success and we need to reload page
        // to get updated students list;
        // reload after 2 seconds, so that user can read success message
        setTimeout(function(){location.reload(true);}, 500);
      }
      $("#load").prop("disabled", false);
    }
  });
}

$(document).ready(function(){
  initUploadStaticData();
});
