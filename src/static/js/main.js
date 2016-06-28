function onOffSubMenu() {
  var menuElem = document.getElementById('sweeties');
  var titleElem = document.getElementById('title');

  titleElem.onclick = function() {
    $('#icon_static').toggleClass("fa-chevron-right", "fa-chevron-down");
    $('#icon_static').toggleClass("fa-chevron-down", "fa-chevron-right");
    $('#sweeties').toggleClass("sub-menu-visible", "sub-menu-no-visible");
    $('#sweeties').toggleClass("sub-menu-no-visible", "sub-menu-visible");
  };
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

function invisibleSelect() {
  $("select").selecter();
  //$("select").dropdown();
}

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
    $('div.available div.multiple select option').attr("selected", "selected");
    $('div.available div.multiple div.selecter-options span.selecter-item').attr("class", "selecter-item selected");
  });
}

function selectAllChosen() {
  $('#select-chosen-files option').each(function(){
    $('div.chosen div.multiple select option').attr("selected", "selected");
    $('div.chosen div.multiple div.selecter-options span.selecter-item').attr("class", "selecter-item selected");
  });
}

//function changeColorTyping(obj) {
//  //var elems = $('div .form-control');
//  //var elemsTotal = elems.length;
//  alert('VAL = '+$(obj).val());
//
//  if ($(obj).val()) {
//    $($(obj)).toggleClass('field-success');
//  }
//
//
//  //removeClass
//
//  //for(var i = 0; i < elemsTotal; ++i){
//  //  if ($(elems[i]).val()){
//  //    $(elems[i]).toggleClass('field-success');
//  //
//  //    if ($(elems[i]).nextAll().length > 0){
//  //      if ($(elems[i]).nextAll().hasClass('selecter-selected')){
//  //        $(elems[i]).nextAll().toggleClass('field-success');
//  //        //alert('SELECT!');
//  //      }
//  //    }
//  //  }
//  //}
//}

function visibleDoy(){
  var doyElement = $('span.field-success').html();

  if (doyElement === 'Input a variable'){
    //$('.doy').attr('disabled', false);
    $(".doy-label").removeClass("disabled");
    $(".doy").removeClass("disabled");
    //$(".doy-label").removeClass("disabled-doy");
    $(".doy-label").addClass("visible");
    $(".doy").addClass("visible");
    //$(".doy-label").addClass("visible-doy");
  } else {
    //$('.doy').attr('disabled', true);
    //$(".doy-label").removeClass("visible-doy");
    $(".doy").removeClass("visible");
    $(".doy-label").removeClass("visible");
    $(".doy").addClass("disabled");
    $(".doy-label").addClass("disabled");
    //$(".doy-label").addClass("disabled-doy");
  };
}

function statusPeriod(){
  var periodElement = $('span.field-success').html();

  if (periodElement === 'Input a variable'){
    $(".doy").removeClass("disabled");
    $(".doy-label").removeClass("disabled");
    $(".doy").addClass("visible");
    $(".doy-label").addClass("visible");


    //$('.doy').attr('disabled', false);
    //$(".doy-label").removeClass("disabled-doy");
    //$(".doy-label").addClass("visible-doy");
  } else {
    $(".doy").removeClass("visible");
    $(".doy-label").removeClass("visible");
    $(".doy").addClass("disabled");
    $(".doy-label").addClass("disabled");

    //$('.doy').attr('disabled', true);
    //$(".doy-label").removeClass("visible-doy");
    //$(".doy-label").addClass("disabled-doy");
  };

  //alert(periodElement);
}


$(document).ready(function(){
  //selectAll();
  onOffSubMenu();
  invisibleDropMenu();
  onOffSubMenuUser();
  invisibleSelect();
  changeColorError();
  changeColorSuccess();
  colorBlackSelect();
  statusPeriod();
});