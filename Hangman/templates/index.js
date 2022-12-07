var register_button = document.getElementById("register");
var login_button = document.getElementById("login");

register_button.addEventListener("click", register_function);
login_button.addEventListener("click", login_function);

function register_function() {
  window.location.href = "registration_form/registration_form.html";
}

function login_function() {
  window.location.href = "login_form/login_form.html";
}
