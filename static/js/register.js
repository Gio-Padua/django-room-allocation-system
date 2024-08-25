const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const passwordField = document.querySelector("#passwordField");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

document.addEventListener('DOMContentLoaded', function() {
  const showPasswordToggle = document.querySelector("#showPasswordToggle");

  if (showPasswordToggle) {
      showPasswordToggle.addEventListener("click", handleToggleInput);
  } else {
      console.error("Element with class 'showPasswordToggle' not found.");
  }
});

const handleToggleInput = () => {
  const passwordField = document.getElementById('passwordField');
  if (passwordField) {
      if (passwordField.type === "password") {
          passwordField.type = "text";
      } else {
          passwordField.type = "password";
      }
  } else {
      console.error("Element with ID 'passwordField' not found.");
  }
};

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/auth/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.email_error) {
          submitBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {

  let listNames = ["Tilen","Marko","Teja","Tisa","Rok","Luka","Mojca"];


  if (usernameField.value.length <= 20 && usernameField.value.length >= 3) {} else {
    alert("Username has to be between 3-20 characters.")
  }


  for (let i = 0; i < listNames.length; i++) {
    if (listNames[i] === usernameField.value) {
      alert('The name already exist')
    }
  }
  return false;
});