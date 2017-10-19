// dropdawn menu Setup Static Data
function onOffSubMenuSetupStaticData() {
    var menuElem = document.getElementById('sweeties');
    var titleElem = document.getElementById('title');

    if (titleElem) {
        titleElem.onclick = function() {
            $('#icon_static').toggleClass("fa-chevron-right", "fa-chevron-down");
            $('#icon_static').toggleClass("fa-chevron-down", "fa-chevron-right");
            $('#sweeties').toggleClass("sub-menu-visible", "sub-menu-no-visible");
            $('#sweeties').toggleClass("sub-menu-no-visible", "sub-menu-visible");

            $('#icon_static2').removeClass("fa-chevron-down");
            $('#sweeties2').removeClass("sub-menu-visible");

            $('#icon_static2').addClass("fa-chevron-right");
            $('#sweeties2').addClass("sub-menu-no-visible");
        };
    }
}

// dropdawn menu Upload Test Data
function onOffSubMenuUploadTestData() {
  var menuElem = document.getElementById('sweeties2');
  var titleElem = document.getElementById('title2');

  if (titleElem) {
    titleElem.onclick = function() {
        $('#icon_static2').toggleClass("fa-chevron-right", "fa-chevron-down");
        $('#icon_static2').toggleClass("fa-chevron-down", "fa-chevron-right");
        $('#sweeties2').toggleClass("sub-menu-visible", "sub-menu-no-visible");
        $('#sweeties2').toggleClass("sub-menu-no-visible", "sub-menu-visible");

        $('#icon_static').removeClass("fa-chevron-down");
        $('#sweeties').removeClass("sub-menu-visible");

        $('#icon_static').addClass("fa-chevron-right");
        $('#sweeties').addClass("sub-menu-no-visible");
    };
  }
}

function onOffSubMenuUser() {
    var menuElem = document.getElementById('dropUser');
    var titleElem = document.getElementById('titleUser');
    
    if (titleElem) {
        titleElem.onclick = function() {
            menuElem.classList.toggle('open');
            $(".icon-visible-user").toggle();
            document.getElementById("dropdownUser").classList.toggle("show");
        };
    }
}

function showSubMenuUser() {
  document.getElementById("dropdownUser").classList.toggle("show");
}

function invisibleDropMenu() {
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn-user')) {
      var dropdowns = document.getElementsByClassName("dropdown-content-user");
      var i;
      event = event || window.event;
      var target = event.target || event.srcElement;

      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];

        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
          $(".icon-visible-user").toggle();
        }
      }
    }
  }
}

// function invisibleSelect() {
//   $("select").selecter();
// }

function changeColorError() {
  if ( $('span').is('.field-error') ) {
    $('span.field-error > .form-control').toggleClass('field-error');
    $('span.field-error > div.selecter > .selecter-selected').toggleClass('field-error');
  }
}

function changeColorSuccess() {
  var elems = $('div .form-control');
  var elemsTotal = elems.length;

  for(var i = 0; i < elemsTotal; ++i){
    if ($(elems[i]).val()){
      $(elems[i]).toggleClass('field-success');
    }
  }
}

function colorBlackSelect() {
  var select_item = $('span.selecter-selected');
  var select_total = select_item.length;

  for(var i = 0; i < select_total; ++i) {
    var select_text = $(select_item[i]).text();

    if (select_text.indexOf('Select') < 0){
      $(select_item[i]).toggleClass('color-222');
      $(select_item[i]).toggleClass('field-success');
    } else {
      $(select_item[i]).toggleClass('color-999');
      $(select_item[i]).removeClass('field-success');
    }
  }
}

function selectAllAvialable() {
  $('#select-available-files option').each(function(){
    $(this).attr("selected", "selected");
  });
}

function selectAllChosen() {
  $('#select-chosen-files option').each(function(){
    $(this).attr("selected", "selected");
  });
}

function visibleDoy(){
  var doyElement = $('span.field-success').html();

  if (doyElement === 'Input a variable'){
    $(".doy-label").removeClass("disabled");
    $(".doy").removeClass("disabled");
    $(".doy-label").addClass("visible");
    $(".doy").addClass("visible");
  } else {
    $(".doy").removeClass("visible");
    $(".doy-label").removeClass("visible");
    $(".doy").addClass("disabled");
    $(".doy-label").addClass("disabled");
  };
}

function statusPeriod(){
  var periodElement = $('span.field-success').html();

  if (periodElement === 'Input a variable'){
    $(".doy").removeClass("disabled");
    $(".doy-label").removeClass("disabled");
    $(".doy").addClass("visible");
    $(".doy-label").addClass("visible");
  } else {
    $(".doy").removeClass("visible");
    $(".doy-label").removeClass("visible");
    $(".doy").addClass("disabled");
    $(".doy-label").addClass("disabled");
  };
}

function getRandomArbitary(min, max){
  return Math.random() * (max - min) + min;
}

function addRunCardItem(){
  var select = $("#carditem_all option:selected").text();
  var select_val = $("#carditem_all option:selected").val();
  var order = $("input#order_carditem").val();
  var id_str = new String(getRandomArbitary(1, 10000)).replace(/\./g, "");
  var indetificator = Number(id_str);

  $("tbody").append('<tr id="'+indetificator+'"></tr>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'"><input type="checkbox" name="carditem_select" value="'+select_val+'" class="select_item" checked></td>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'">'+select+'</td>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'" name="carditem_order"><input type="text" class="center non-input" name="carditem_order" value="'+order+'" class="select_item"</td>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'"><button class="btn del-btn check-cur-delete" type="button" name="del_current_btn" value="'+indetificator+'" onclick="deleteCurrentCardItem('+indetificator+')"><img src="/static/img/delete-18.png"/></button></td>');
}

function deleteCurrentCardItem(item){
  var name = new String(item);

  $("tr#"+item).detach();
  $("td."+item).detach();
}

// initial tooltip for bootstrap
function initTooltipBootstrap(){
    $('[data-toggle="tooltip"]').tooltip();
}

function initCreateCard(){
    $('button.create_card').click(function(event){
        var modal = $('#modalCreateCard');
        modal.modal('show');
    });
}

function initSelectConfigFile(){
    var config_file = $('#id_configfile');
    $('div#select-files > div.selecter > div.selecter-options > span.selecter-item').click(function(event){
        var select = $(this).text();
        $(this).removeClass("selecter-item");
        $(this).addClass("selecter-item selected");
        $(this).attr("name", "select-file");
        $(config_file).val(select);
    });
}

function initAddFormatingTextarrea(){
    // textarea
    $("#div_id_content > div.controls").addClass("textarea");
}

function greyColorSelect() {
    var select_option = $("select.form-control option");
    var select_selected = $("select.form-control :selected");
    var select = $("select.form-control");
    
    $(select_selected).each(function(){
        if (this.text == 'Select') {
            // alert('Select: '+this.text);
            $(select).addClass('font-color-grey');
        }
    });
    
    $(select_option).each(function(){
        if (this.text == 'Select') {
            $(this).addClass('font-color-grey');
        }
    });
}

function setDataSetInfoPanel() {
    var select_dataset = $("#mydataset option:selected");
    var info_dataset = $("span#show_info_dataset");
    var current_dataset = select_dataset.html();
    $(info_dataset).html(current_dataset);
}

function setImageInfoPanel() {
    var select_dataset = $("#mydataset option:selected");
    var info_dataset = $("span#show_info_image");
    var current_dataset = select_dataset.html();
    $(info_dataset).html(current_dataset);
}

function resizeScreen() {
    var width = window.innerWidth;
    var div_map = document.getElementById('map');
    var col1 = document.getElementById('col1');
    // var col2 = document.getElementById('col2');
    var get_status_message = getUrlVars()["status_message"];
    
    // alert('GET: '+getUrlVars()["id"]);
    // alert('Width = '+window.innerWidth + '. Height = '+window.innerHeight);
    
    if (div_map) {
        if (width < '1355') {
            div_map.style.width = "103%";
            div_map.style.height = "750px";
            
            if (get_status_message) {
                col1.style.height = "1030px";
                // col2.style.height = "1030px";
            } else {
                col1.style.height = "870px";
                // col2.style.height = "870px";
            }
        } else if (width >= '1355' && width <= '1800') {
            div_map.style.width = "102%";
            div_map.style.height = "960px";
            
            if (get_status_message) {
                col1.style.height = "1105px";
                // col2.style.height = "1105px";
            } else {
                col1.style.height = "1045px";
                // col2.style.height = "1045px";
            }
        } else {
            div_map.style.width = "101%";
            div_map.style.height = "1200px";
            
            if (get_status_message) {
                col1.style.height = "1345px";
                // col2.style.height = "1345px";
            } else {
                col1.style.height = "1285px";
                // col2.style.height = "1285px";
            }
        }
    }
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m, key, value) {
        vars[key] = value;
    });
    return vars;
}

function selectAllCheck(field, flag) {
    if (flag == "1") {
        for (i=0; i<field.length; i++) {
            field[i].checked = true;
        }
    }
    else {
        for (i=0; i<field.length; i++) {
            field[i].checked = false;
        }
    }

    var is_ts_checked = $('#ts input:checkbox:checked');

    if (is_ts_checked.val()) {
        $('#ts input:checkbox:checked').each(function(){
            // alert($(this).val());
            $('#draw_plot').removeAttr('disabled');
        });
    } else {
        $('#draw_plot').attr('disabled','disable');
    }
}

function setStatic() {
    $('#statictics_list label input:radio').click(function () {
        var value = $(this).val();
        $("span#stat_show").text(value);
    });
}

function getFileName() {
    $('input[type="file"]').on('change', function (event, files, label) {
        var file_name = document.getElementById('id_test_data').files[0].name;
        $('span.file-selected').text(file_name);
        // alert('FILE 2: '+span_obj);
    });
}

function toggleScale() {
    var scale = document.getElementById('scale_id');

    if (scale.style.visibility == "hidden") {
        scale.style.visibility = "visible";
    } else {
        scale.style.visibility = "hidden";
    }
}

function go_progress_ts() {
    // console.log('showWaiting COUNT TS: '+count_ts);

    progress = parseFloat((progress + time_section).toFixed(1));

    // console.log('1 GO progress TS: ', progress);
    console.log('1 GO time_section: ', time_section);

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

function showWaiting() {
    // console.log('showWaiting COUNT TS: '+count_ts);
    // debugger;
    // console.time('test');

    // clearInterval(timerId);
    // progress = 0;
    // time_section = 0;

    var modal = $('#modalWaiting');
    // var modal = document.getElementById('modalWaiting_1');
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
        go_progress_ts();
    }, time_interval);

    // console.timeEnd('showWaiting: ', count_ts);
}

function toogleVisibleDrawPlot() {
    var is_ts_checked = $('#ts input:checkbox:checked');

    if (is_ts_checked.val()) {
        $('#ts input:checkbox:checked').each(function(){
            // alert($(this).val());
            $('#draw_plot').removeAttr('disabled');
        });
    } else {
        $('#draw_plot').attr('disabled','disable');
    }
}

function toogleHidenTsName(obj) {
    console.log('toogleHidenTsName: ', obj.checked);
    var is_check = obj.checked;

    if (is_check) {
        // console.log('YES');
        $('#id_name_ts').removeAttr('disabled');
    } else {
        // console.log('NO');
        $('#id_name_ts').attr('disabled','disable');
    }
}

function checkIsCheck() {
    var is_check = $('#id_is_ts').attr('checked');

    // console.log('IS CHECK: ', is_check);

    if (is_check) {
        // console.log('YES');
        $('#id_name_ts').removeAttr('disabled');
    } else {
        // console.log('NO');
        $('#id_name_ts').attr('disabled','disable');
    }
}

function selectAoi() {
    // alert('select_aoi: '+select_aoi);
    // console.log('select_aoi: ', select_aoi);
    if (select_aoi) {
        var aoi_list = select_aoi.split(',')
        // for (i = 0; i < select_aoi.length; i++) {
        //     alert('selectedAoi: '+select_aoi[i]);
        // }
        
        // console.log('aoi_list: ', aoi_list);
        
        $('#select_aoi').selectpicker('val', aoi_list);
    }
}

function selectedAoi() {
    if ($('#select_aoi').val()) {
        console.log('YES');
        var list_aoi = $('#select_aoi').val();
        var start_title = '';

        for (var m = 0; m < list_aoi.length; m++) {
            console.log('list_aoi: ', list_aoi[m]);

            var aoi_tmp = list_aoi[m].split('_');
            
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

    $('#aoi_selected span').text(start_title);

    // alert('select_aoi: '+list_aoi);
    console.log('selectedAoi select_aoi: ', list_aoi);
}

// function getFileNames() {
//     var upload = document.getElementsByClassName("no-file-selected");

//     return Array.prototype.map.call(upload.files, function(file) {
//         return file.name;
//     });

//     upload.onchange = function() {
//         alert(getFileNames());
//     }
// }




$(document).ready(function(){
    //selectAll();
    onOffSubMenuSetupStaticData();
    onOffSubMenuUploadTestData();
    invisibleDropMenu();
    onOffSubMenuUser();
    // invisibleSelect();
    changeColorError();
    changeColorSuccess();
    colorBlackSelect();
    statusPeriod();
    initTooltipBootstrap();
    initCreateCard();
    initSelectConfigFile();
    initAddFormatingTextarrea();
    greyColorSelect();
    setDataSetInfoPanel();
    setImageInfoPanel();
    resizeScreen();
    setStatic();
    // get_file_name();
    toogleVisibleDrawPlot();
    getFileName();

    if (select_aoi) {
        selectAoi();
    }

    checkIsCheck();

    // selectedAoi();
    
    // tabsCustomerMenu();
    // showCheckboxes();
});
