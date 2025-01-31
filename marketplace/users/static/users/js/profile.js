// Функция для отображения/скрытия формы имени
const editUsernameBtn = document.getElementById("edit-username-btn");
const usernameForm = document.getElementById("username-form");
const usernameDisplay = document.getElementById("username-display");
const cancelUsernameBtn = document.getElementById("cancel-username-btn");

editUsernameBtn.addEventListener("click", () => {
    usernameForm.style.display = "block";
    usernameDisplay.style.display = "none";
    editUsernameBtn.style.display = "none";
});

cancelUsernameBtn.addEventListener("click", () => {
    usernameForm.style.display = "none";
    usernameDisplay.style.display = "block";
    editUsernameBtn.style.display = "block";
});

// Функция для отображения/скрытия формы почты
const editEmailBtn = document.getElementById("edit-email-btn");
const emailForm = document.getElementById("email-form");
const emailDisplay = document.getElementById("email-display");
const cancelEmailBtn = document.getElementById("cancel-email-btn");

editEmailBtn.addEventListener("click", () => {
    emailForm.style.display = "block";
    emailDisplay.style.display = "none";
    editEmailBtn.style.display = "none";
});

cancelEmailBtn.addEventListener("click", () => {
    emailForm.style.display = "none";
    emailDisplay.style.display = "block";
    editEmailBtn.style.display = "block";
});