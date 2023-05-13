
function checkPasswordStrength(password) {
    var lowercaseLabel = document.getElementById("lowercase-label");
    var uppercaseLabel = document.getElementById("uppercase-label");
    var letterLabel = document.getElementById("letter-label");
    var lengthLabel = document.getElementById("length-label");

    var lowercaseRegex = /[a-z]/;
    var uppercaseRegex = /[A-Z]/
    var letterRegex = /[a-zA-Z]/;
    var lengthRegex = /.{8,}/;

    if (lowercaseRegex.test(password)) {
        lowercaseLabel.classList.remove("red-label");
        lowercaseLabel.classList.add("green-label");
    } else {
        lowercaseLabel.classList.remove("green-label");
        lowercaseLabel.classList.add("red-label");
    }

    if (uppercaseRegex.test(password)) {
        uppercaseLabel.classList.remove("red-label");
        uppercaseLabel.classList.add("green-label");
    } else {
        uppercaseLabel.classList.remove("green-label");
        uppercaseLabel.classList.add("red-label");
    }

    if (letterRegex.test(password)) {
        letterLabel.classList.remove("red-label");
        letterLabel.classList.add("green-label");
    } else {
        letterLabel.classList.remove("green-label");
        letterLabel.classList.add("red-label");
    }

    if (lengthRegex.test(password)) {
        lengthLabel.classList.remove("red-label");
        lengthLabel.classList.add("green-label");
    } else {
        lengthLabel.classList.remove("green-label");
        lengthLabel.classList.add("red-label");
    }
}
