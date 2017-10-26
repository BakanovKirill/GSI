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


$(document).ready(function(){
    getFileName();
});
