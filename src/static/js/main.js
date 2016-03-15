function setFocus() {
  document.getElementById("login").focus();
  //$("span.img-top-input").css('display', 'block');
}

function visiblePasswordTopInput() {
  $('.pass').css('display', 'block');
  var x = document.getElementById("password");

  if (x.value == '') {
    $('.pass').css('display', 'none');
  }
}

function visibleRePasswordTopInput() {
  $('.re-pass').css('display', 'block');

  var x = document.getElementById("re-password");

  if (x.value == '') {
    $('.re-pass').css('display', 'none');
  }
}

function visibleUsernameTopInput() {
  $('.username').css('display', 'block');

  var x = document.getElementById("login");

  if (x.value == '') {
    $('.username').css('display', 'none');
  }
}

function visibleEmailTopInput() {
  $('.email').css('display', 'block');

  var x = document.getElementById("email");

  if (x.value == '') {
    $('.email').css('display', 'none');
  }
}


$(document).ready(function(){
  setFocus();
  //visiblePasswordTopInput()
});