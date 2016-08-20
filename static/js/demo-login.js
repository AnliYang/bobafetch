function autofillDemo() {
  autofillCredentials();
  updateLogin();
}

function autofillCredentials() {
  $('#email').val('demo@bobafetch.com');
  $('#password').val('bobafetch');
}

function updateLogin() {
  $('#login').removeClass('btn-default');
  $('#login').addClass('btn-success');
}

$('#demo').click(autofillDemo);
