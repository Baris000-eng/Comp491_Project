var brightnessSlider = document.getElementById("brightnessSlider");
var bodyElement = document.getElementsByTagName("body")[0];
var myHeading = document.getElementsByTagName("h2")[0];
var myHeading2 = document.getElementsByTagName('h4')[0];
var myHeading3 = document.getElementsByTagName('h4')[1];
var myHeading4 = document.getElementsByTagName('h4')[2];
var myHeading5 = document.getElementsByTagName('h4')[3];


brightnessSlider.addEventListener("input", function () {
        var brightnessValue = this.value;
        var cssRule = "background-color: hsl(0, 0%, " + brightnessValue + "%);";
        bodyElement.style.cssText += cssRule;
        if (brightnessValue >= 50) {
            bodyElement.style.color = "black";
            myHeading.style.color = 'black';
            myHeading2.style.color = 'black';
            myHeading3.style.color = 'black';
            myHeading4.style.color = 'black';
            myHeading5.style.color = 'black';
        } else {
            bodyElement.style.color = "white";
            myHeading.style.color = 'white';
            myHeading2.style.color = 'white';
            myHeading3.style.color = 'white';
            myHeading4.style.color = 'white';
            myHeading5.style.color = 'white';
        }


});

var bgColorSelector = document.getElementById("bgColorSelector");
var applyBgColorButton = document.querySelector("button");

applyBgColorButton.addEventListener("click", function () {
        var bgColor = bgColorSelector.value;
        bodyElement.style.backgroundColor = bgColor;
});

bgColorSelector.addEventListener("change", function () {
        var bgColor = bgColorSelector.value;
        bodyElement.style.backgroundColor = bgColor;
});

function applyBgColor() {
        var bgColor = bgColorSelector.value;
        bodyElement.style.backgroundColor = bgColor;
}


var audioElement = document.createElement("audio");
audioElement.src = "../static/c.mp3";
audioElement.loop = true;

function playMusic() {
        audioElement.play(); // play the audio music
}

function stopMusic() {
        audioElement.currentTime = 0;  // Reset the audio to the beginning
        audioElement.pause();          // Pause the audio music
}

function pauseMusic() {
        audioElement.pause(); // pausing the audio music
}


var darkModeToggle = document.getElementById("darkModeToggle");
var bodyElement = document.getElementsByTagName("body")[0];

darkModeToggle.addEventListener("change", function () {
        if (this.checked) {
            bodyElement.style.backgroundColor = "#333";
            bodyElement.style.color = "white";
        } else {
            bodyElement.style.backgroundColor = "white";
            bodyElement.style.color = "#333";
        }
});
