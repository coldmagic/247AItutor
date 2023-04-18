// /static/js/validation.js

// Function to validate an email address
function validateEmail(email) {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}

// Function to validate login form fields
function validateLoginForm() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const errorElement = document.getElementById('form-error');

  if (!email || !password) {
    errorElement.textContent = 'All fields are required';
    return false;
  }

  if (!validateEmail(email)) {
    errorElement.textContent = 'Invalid email format';
    return false;
  }

  return true;
}

// Function to validate registration form fields
function validateRegisterForm() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const errorElement = document.getElementById('form-error');

  if (!name || !email || !password) {
    errorElement.textContent = 'All fields are required';
    return false;
  }

  if (!validateEmail(email)) {
    errorElement.textContent = 'Invalid email format';
    return false;
  }

  return true;
}
