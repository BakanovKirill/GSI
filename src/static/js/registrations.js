function setFocus() {
  document.getElementById("username").focus();
}

// function visibleUsernameTopInput() {
//   $('.username').css('display', 'none');
//   var username = document.getElementById("username");
//
//   if (username.value === '') {
//     $('.username').css('display', 'none');
//   }
//   else {
//      $('.username').css('display', 'block');
//   }
// }
//
function visiblePasswordTopInput() {
  $('.pass').css('display', 'none');
  var pass = document.getElementById("id_new_password1");

  if (pass.value === '') {
    $('.pass').css('display', 'none');
  }
  else {
     $('.pass').css('display', 'block');
  }
}
//
// function visibleRePasswordTopInput() {
//   $('.re-pass').css('display', 'none');
//   var re_pass = document.getElementById("id_new_password2");
//
//   if (re_pass.value === '') {
//     $('.re-pass').css('display', 'none');
//   }
//   else {
//      $('.re-pass').css('display', 'block');
//   }
// }
//
// function visibleEmailTopInput() {
//   $('.email').css('display', 'none');
//   var email = document.getElementById("id_email");
//
//   if (email.value === '') {
//     $('.email').css('display', 'none');
//   }
//   else {
//      $('.email').css('display', 'block');
//   }
// }

function addClassEmailField() {
  // $("input#id_email").addClass("border-bottom form-control padding-0");
  $("input#id_email").attr("placeholder", "Enter your email address below");

  $('input#id_email').on('input', function(){ visibleEmailTopInput() });
  $('input#id_email').on('keyup', function(){ visibleEmailTopInput() });
}

function addClassPasswordField() {
  // $("input#id_new_password1").addClass("border-bottom form-control padding-0 form-password");
  $("input#id_new_password1").attr("placeholder", "New password");
  
  $('input#id_new_password1').on('input', function(){ visiblePasswordTopInput()() });
  $('input#id_new_password1').on('keyup', function(){ visiblePasswordTopInput() });


  // $("input#id_new_password2").addClass("border-bottom form-control padding-0 input-form");
  $("input#id_new_password2").attr("placeholder", "Confirm password");

  $('input#id_new_password2').on('input', function(){ visibleRePasswordTopInput()() });
  $('input#id_new_password2').on('keyup', function(){ visibleRePasswordTopInput() });
}


$(document).ready(function(){
  if ($("input").is("#username") == true) {
    setFocus();
  }
  addClassEmailField();
  addClassPasswordField();
});
