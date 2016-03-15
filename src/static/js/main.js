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

function visibleLoginIcons() {
  var password = document.getElementById("password");
  var login = document.getElementById("login");

  if (password.value !== ' ') {
    $('.pass').css('display', 'block');
  }

  if (login.value !== ' ') {
    $('.username').css('display', 'block');
  }
}


function visibleRegistrationIcons() {
  var email = document.getElementById("email");
  var login = document.getElementById("login");

  if (email.value !== null) {
    $('.email').css('display', 'block');
  }

  if (login.value !== ' ') {
    $('.username').css('display', 'block');
  }
}


$(document).ready(function(){
  setFocus();
});