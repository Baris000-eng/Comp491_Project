document.addEventListener("mousemove", function (event) {
  var cursorLabel = document.getElementById("cursor-label");
  var mapContainer = document.getElementById("map-container");

  var rect = mapContainer.getBoundingClientRect();

  var xCoordinate = event.clientX - rect.left;
  var yCoordinate = event.clientY - rect.top;

  if (
      xCoordinate > 1500 && 
      xCoordinate < 1800 && 
      yCoordinate > 100 && 
      yCoordinate < 250
  ) {
      cursorLabel.textContent = "Click here to Reserve a classroom inside SNA";
  } 
  else if (
      xCoordinate > 0 && 
      xCoordinate < 640 && 
      yCoordinate > 460 && 
      yCoordinate < 880
  ) {
      cursorLabel.textContent = "You are on the dorms";
  } 
  else if (
      xCoordinate > 1196 && 
      xCoordinate < 1532 && 
      yCoordinate > 460 && 
      yCoordinate < 710
  ) {
      cursorLabel.textContent = "You are on the library";
  } 
  else if (
      xCoordinate > 1460 && 
      xCoordinate < 1900 && 
      yCoordinate > 500 && 
      yCoordinate < 790
  ) {
      cursorLabel.textContent = "You are on the Case building";
  } 
  else if (
      xCoordinate > 2320 && 
      xCoordinate < 2630 && 
      yCoordinate > 400 && 
      yCoordinate < 600
  ) {
      cursorLabel.textContent = "You are on the Engineering building";
  } 
  else if (
      xCoordinate > 2100 && 
      xCoordinate < 2350 && 
      yCoordinate > 290 && 
      yCoordinate < 430
  ) {
      cursorLabel.textContent = "You are on the SNA A building";
  } 
  else if (
    xCoordinate > 2130 && 
    xCoordinate < 2400 && 
    yCoordinate > 240 && 
    yCoordinate < 370
  ) {
      cursorLabel.textContent = "You are on the SNA B building";
  } 
  else if (
    xCoordinate > 2130 && 
    xCoordinate < 2400 && 
    yCoordinate > 430 && 
    yCoordinate < 850
  ) {
      cursorLabel.textContent = "You are on the SOS building";
  } 
  else if (
    xCoordinate > 2020 && 
    xCoordinate < 2500 && 
    yCoordinate > 420 && 
    yCoordinate < 720
  ) {
      cursorLabel.textContent = "You are on the SCI building";
  } 
  else if (
    xCoordinate > 1350 && 
    xCoordinate < 1600 && 
    yCoordinate > 400 && 
    yCoordinate < 560
  ) {
      cursorLabel.textContent = "You are on the ELC building";
  } 
  else if (
    xCoordinate > 900 && 
    xCoordinate < 1400 && 
    yCoordinate > 750 && 
    yCoordinate < 1080
  ) {
      cursorLabel.textContent = "You are on the STD building";
  } 
  else {
      cursorLabel.textContent = "X: " + xCoordinate + ", Y: " + yCoordinate;
  }

  cursorLabel.style.top = (yCoordinate + 10) + "px";
  cursorLabel.style.left = (xCoordinate + 10) + "px";
});

function redirect(pageUrl) {
  window.location.href = pageUrl;
}
