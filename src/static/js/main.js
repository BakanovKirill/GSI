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
    //document.getElementById("dropdownMenu").classList.toggle("show");
  };
}

function showSubMenu() {
  document.getElementById("dropdownMenu").classList.toggle("show");
}

function showSubMenuUser() {
  document.getElementById("dropdownUser").classList.toggle("show");
  //document.getElementById("dropdownUser").classList.toggle("show");
  //$(".icon-visible-user").toggle();
}

function invisibleDropMenu() {
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      event = event || window.event;
      var target = event.target || event.srcElement;
      //var fa_class = target.className;
      //var fa_elem = document.getElementsByClassName(fa_class > i);
      //var fa_down = document.getElementsByClassName('fa-chevron-down');

      //alert(fa_elem === fa_down);

      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];

        if (openDropdown.classList.contains('show') && target.id !== "title") {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
}

$(document).ready(function(){
  onOffSubMenu();
  invisibleDropMenu();
  onOffSubMenuUser();
});