document.addEventListener("mousemove", function (event) {
  var cursorLabel = document.getElementById("cursor-label");
  var xCoordinate = event.clientX;
  var yCoordinate = event.clientY;

  if (
    xCoordinate > 1500 &&
    xCoordinate < 1800 &&
    yCoordinate > 100 &&
    yCoordinate < 250
  ) {
    if (xCoordinate < 1800) {
      if (yCoordinate > 100) {
        if (yCoordinate < 250) {
          cursorLabel.textContent =
            "Click here to Reserve a classroom inside SNA";
        } else {
          cursorLabel.textContent =
            "X: " + event.clientX + ", Y: " + event.clientY;
        }
      } else {
        cursorLabel.textContent =
          "X: " + event.clientX + ", Y: " + event.clientY;
      }
    } else {
      cursorLabel.textContent = "X: " + event.clientX + ", Y: " + event.clientY;
    }
  } else if (
    xCoordinate > 0 &&
    xCoordinate < 520 &&
    yCoordinate > 240 &&
    yCoordinate < 580
  ) {
    if (xCoordinate < 520) {
      if (yCoordinate > 240) {
        if (yCoordinate < 580) {
          cursorLabel.textContent = "You are on the dorms";
        } else {
          cursorLabel.textContent =
            "X: " + event.clientX + ", Y: " + event.clientY;
        }
      } else {
        cursorLabel.textContent =
          "X: " + event.clientX + ", Y: " + event.clientY;
      }
    } else {
      cursorLabel.textContent = "X: " + event.clientX + ", Y: " + event.clientY;
    }
  } else if (
    xCoordinate > 900 &&
    xCoordinate < 1100 &&
    yCoordinate > 220 &&
    yCoordinate < 430
  ) {
    cursorLabel.textContent = "You are on the library";
  } else if (
    xCoordinate > 1100 &&
    xCoordinate < 1390 &&
    yCoordinate > 295 &&
    yCoordinate < 500
  ) {
    cursorLabel.textContent = "You are on the Case building";
  } else if (
    xCoordinate > 1460 &&
    xCoordinate < 1750 &&
    yCoordinate > 414 &&
    yCoordinate < 550
  ) {
    cursorLabel.textContent = "You are on the Engineering building";
  } else if (
    xCoordinate > 1460 &&
    xCoordinate < 1750 &&
    yCoordinate > 414 &&
    yCoordinate < 550
  ) {
    cursorLabel.textContent = "You are on the SNA building";
  } else if (
    xCoordinate > 1460 &&
    xCoordinate < 1750 &&
    yCoordinate > 414 &&
    yCoordinate < 550
  ) {
    cursorLabel.textContent = "You are on the Engineering building";
  } else {
    cursorLabel.textContent = "X: " + event.clientX + ", Y: " + event.clientY;
  }

  cursorLabel.style.top = event.clientY + 10 + "px";
  cursorLabel.style.left = event.clientX + 10 + "px";
});


function redirect(pageUrl) {
    window.location.href = pageUrl;
}
