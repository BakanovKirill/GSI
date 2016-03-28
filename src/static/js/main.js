function onOffSubMenu() {
  var menuElem = document.getElementById('sweeties');
  var titleElem = document.getElementById('title');

  titleElem.onclick = function() {
    menuElem.classList.toggle('open');
    $(".icon-visible").toggle();
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
  document.getElementById("subMenu").classList.toggle("show");
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

$(document).ready(function(){
  onOffSubMenu();
  //invisibleDropMenuUser();
  invisibleDropMenu();
  onOffSubMenuUser();
});