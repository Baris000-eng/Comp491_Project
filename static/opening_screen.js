function changeBackgroundColor(color) {
  document.body.style.backgroundColor = color;
}

document.addEventListener("DOMContentLoaded", function() {
  const images = [
    "../static/images/img1.png",
    "../static/images/img2.png",
    "../static/images/img3.png"
  ];
  
  let currentImageIndex = 0;
  const imageElement = document.querySelector(".image");
  
  setInterval(() => {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    const nextImageSrc = images[currentImageIndex];
    imageElement.setAttribute("src", nextImageSrc);
  }, 1000);
});


