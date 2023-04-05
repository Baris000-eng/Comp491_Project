function hideOrOpenSignupHelp() {
    var signupHelpText = document.getElementById("student-signup-help-text");
    var signupGuideButton = document.getElementById("student-signup-guide");
    if (signupHelpText.style.display === "none") {
        signupHelpText.style.display = "block";
        signupGuideButton.textContent = "Close Student Signup Guide";
        signupGuideButton.style.marginTop = "75px";
    } else {
        signupHelpText.style.display = "none";
        signupGuideButton.textContent = "Open Student Signup Guide";
        signupGuideButton.style.marginTop = "10px";
    }
}