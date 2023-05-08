function activateButton(button) {
  button.disabled = true;
  button.closest("form").submit();
}

document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".buttons button");
  buttons.forEach(function (button) {
      let timeout;
      button.addEventListener("mouseenter", function () {
          timeout = setTimeout(function () {
              activateButton(button);
          }, 2000);
      });
      button.addEventListener("mouseleave", function () {
          clearTimeout(timeout);
      });
  });
});