function getFileName() {
    $('input[type="file"]').on('change', function (event, files, label) {
        var file_name = document.getElementById('id_test_data').files[0].name;
        $('span.file-selected').text(file_name);
        // alert('FILE 2: '+span_obj);
    });
}


$(document).ready(function(){
    getFileName();
});
