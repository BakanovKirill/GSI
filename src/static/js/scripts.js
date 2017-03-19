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

  titleElem.onclick = function() {
    menuElem.classList.toggle('open');
    $(".icon-visible-user").toggle();
    document.getElementById("dropdownUser").classList.toggle("show");
  };
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
    var info_dataset = $("span#info_dataset");
    var current_dataset = select_dataset.html();
    $(info_dataset).html(current_dataset);
}


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
    // showCheckboxes();
});
