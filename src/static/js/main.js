function onOffSubMenu() {
  var menuElem = document.getElementById('sweeties');
  var titleElem = document.getElementById('title');
  //var titleElem = document.getElementsByClassName("title");

  //var i_class = document.getElementsByClassName('icon-visible');
  //var i_style = i_class.style.display;

  titleElem.onclick = function() {
    //alert('i_class ================== '+i_style);
    menuElem.classList.toggle('open');
    $(".icon-visible").toggle();
    //document.getElementById("title").style.color = "#428bca";
  };
}

function showSubMenu() {
  document.getElementById("dropdownMenu").classList.toggle("show");
}

function invisibleDropMenu() {
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      event = event || window.event;
      var target = event.target || event.srcElement;
      var fa_class = target.className;
      var fa_elem = document.getElementsByClassName(fa_class > i);
      var fa_down = document.getElementsByClassName('fa-chevron-down');

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
});