function onOffSubMenu() {
  var menuElem = document.getElementById('sweeties');
  var titleElem = document.getElementById('title');

  titleElem.onclick = function() {
    //menuElem.classList.toggle('open');
    //$(".icon-visible").toggle();
    //if ( $("#sweeties").hasClass("sub-menu-visible") ) {
    //  alert("У элемента задан класс sub-menu-visible!");
    //}

    $('#icon_static').toggleClass("fa-chevron-right", "fa-chevron-down");
    $('#icon_static').toggleClass("fa-chevron-down", "fa-chevron-right");
    $('#sweeties').toggleClass("sub-menu-visible", "sub-menu-no-visible");
    $('#sweeties').toggleClass("sub-menu-no-visible", "sub-menu-visible");
    //$("div.sub-menu-no-visible").toggleClass("sub-menu-visible");
    //$("div.sub-menu-visible").toggleClass("sub-menu-no-visible");

    //$("#sweeties").toggleClass("sub-menu");
    //$("#title").addClass("active-static-data");
    //$("#title").removeClass("li-menu");
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

//function showSubMenu() {
//  document.getElementById("dropdownMenu").classList.toggle("show");
//}

function showSubMenuUser() {
  document.getElementById("dropdownUser").classList.toggle("show");
}

function showSubMenuStaticData() {
  //document.getElementById("subMenu").classList.toggle("show");
  //$("div.sub-menu-no-visible").toggleClass("sub-menu-visible");
}

function invisibleDropMenu() {
  window.onclick = function(event) {
    //if (!event.target.matches('.dropbtn')) {
    //  var dropdowns = document.getElementsByClassName("dropdown-content");
    //  var i;
    //  event = event || window.event;
    //  var target = event.target || event.srcElement;
    //
    //  for (i = 0; i < dropdowns.length; i++) {
    //    var openDropdown = dropdowns[i];
    //
    //    if (openDropdown.classList.contains('show') && target.id !== "title") {
    //      openDropdown.classList.remove('show');
    //      //$(".icon-visible").toggle();
    //      var menuElem = document.getElementById('subMenu');
    //      //menuElem.classList.toggle('hide');
    //    }
    //  }
    //}
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

function chageColorError() {
  if ( $('span').is('.field-error') ) {
    alert('ERROR');
    $('span.field-error > .form-control').toggleClass('field-error');
    $('span.field-error > div.selecter > .selecter-selected').toggleClass('field-error');
  }


  //var elements = $('div .form-control');
  //var elemsTotal = elements.length;
  //alert(elemsTotal);
  //
  //for(var i = 0; i < elemsTotal; ++i){
  //  alert($(elements[i]).val());
  //}
}

$(document).ready(function(){
  onOffSubMenu();
  invisibleDropMenu();
  onOffSubMenuUser();
  invisibleSelect();
  chageColorError();
});