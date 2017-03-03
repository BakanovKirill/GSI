var expanded_statistics = false;
var expanded_root_filenames = false;
var expanded_polygons = false;

function showRootFilenames() {
    showElem("#checkboxes_root_filenames");
}

function hideRootFilenames() {
    hideElem("#select_root_filenames", "#checkboxes_root_filenames");
}

function showStatistics() {
    showElem("#checkboxes_statistics");
}

function hideStatistics() {
    hideElem("#select_statistics", "#checkboxes_statistics");
}

function showPolygons() {
    showElem("#checkboxes_polygons");
}

function hidePolygons() {
    hideElem("#select_polygons", "#checkboxes_polygons");
}

function showElem(checkb) {
    var checkboxes = $(checkb);

    if (checkb == "#checkboxes_root_filenames") {
        if (!expanded_root_filenames) {
            $(checkboxes).show("fast");
            expanded_root_filenames = true;
        } else {
            $(checkboxes).hide("fast");
            expanded_root_filenames = false;
        }
    } else if (checkb == "#checkboxes_statistics") {
        if (!expanded_statistics) {
            $(checkboxes).show("fast");
            expanded_statistics = true;
        } else {
            $(checkboxes).hide("fast");
            expanded_statistics = false;
        }
    } else if (checkb == '#checkboxes_polygons') {
        if (!expanded_polygons) {
            $(checkboxes).show("fast");
            expanded_polygons = true;
        }
        else {
            $(checkboxes).hide("fast");
            expanded_polygons = false;
        }
    }
}

function hideElem(cont, checkb){
    $(document).mouseup(function (e) {
        var container = $(cont);
        var checkboxs = $(checkb);

        if (!container.has(e.target).length){
            $(checkboxs).hide("fast");

            if (checkb == "#checkboxes_root_filenames"){
                expanded_root_filenames = false;
            }

            if (checkb == "#checkboxes_statistics") {
                expanded_statistics = false;
            }

            if (checkb == '#checkboxes_polygons') {
                expanded_polygons = false;
            }
        }
    });
}

function setOpacity() {
    opacity = document.getElementById("opacity").value;
    img = document.getElementById("on_add");
    img.style.opacity = opacity / 100;
    
    var slider_value = $("#slider_value");
    $(slider_value).text('Transparency: '+opacity+' %');

    // alert('setOpacity: '+opacity);
}

// function addChoice(elem) {
//     alert('addChoice: '+$(elem).val());
//     alert('addChoice: '+$('#show_arrea option:selected').val());
//
//     var choice_val = $(elem).val()
//     // var choice = $("#show_arrea");
//     $('div.selecter-options').append( $('<span class="selecter-item" data-value="'+choice_val+'">'+choice_val+'</span>') );
//     $('#choice_p').html(choice_val);
//     // $("select[id=show_arrea]").append('<option value="20">Добавить в самый конец Select</option>')
//     // $('#show_arrea').append('<option value="20">Добавить в самый конец Select</option>');
//     // $("#show_arrea").append('<option value="'+choice_val+'">'+choice_val+'</option>');
// }
//
// function showSelectArea(elem) {
//     // alert('addChoice: ');
// }


$(document).ready(function(){
    hideRootFilenames();
    hideStatistics();
    hidePolygons();
});
