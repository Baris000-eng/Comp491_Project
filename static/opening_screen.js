function changeBackgroundColor(color) {
    document.body.style.backgroundColor = color;
}
document.querySelector('form').addEventListener('submit', function (e) {
// No need to prevent the default behavior
});

function hideOrOpenDescription() {
  var description = document.getElementById("description");
  var button = document.getElementById("description-button");
  if (description.style.display === "none") {
    description.style.display = "block";
    button.textContent = "Hide KuClass Description";
  } else {
    description.style.display = "none";
    button.textContent = "Open KuClass Description";
  }
}

function hideOrOpenHelp() {
  var helpText = document.getElementById("help-text");
  var helpButton = document.getElementById("help-button");
  if (helpText.style.display === "none") {
    helpText.style.display = "block";
    helpButton.textContent = "Hide KuClass Help";
  } else {
    helpText.style.display = "none";
    helpButton.textContent = "Open KuClass Help";
  }
}