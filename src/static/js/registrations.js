function setFocus() {
  document.getElementById("username").focus();
}

function visibleUsernameTopInput() {
  $('.username').css('display', 'none');
  var username = document.getElementById("username");

  if (username.value === '') {
    $('.username').css('display', 'none');
  }
  else {
     $('.username').css('display', 'block');
  }
}

function visiblePasswordTopInput() {
  $('.pass').css('display', 'none');
  var pass = document.getElementById("password");

  if (pass.value === '') {
    $('.pass').css('display', 'none');
  }
  else {
     $('.pass').css('display', 'block');
  }
}

function visibleRePasswordTopInput() {
  $('.re-pass').css('display', 'none');
  var re_pass = document.getElementById("re-password");

  if (re_pass.value === '') {
    $('.re-pass').css('display', 'none');
  }
  else {
     $('.re-pass').css('display', 'block');
  }
}

function visibleEmailTopInput() {
  $('.email').css('display', 'none');
  var email = document.getElementById("email");

  if (email.value === '') {
    $('.email').css('display', 'none');
  }
  else {
     $('.email').css('display', 'block');
  }
}

$(document).ready(function(){
  setFocus();
});