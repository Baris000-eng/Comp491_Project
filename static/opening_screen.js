document.addEventListener("DOMContentLoaded", function () {
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

setInterval(function () {
  var selectedRole = document.querySelector('input[type=radio]:checked');
  if (selectedRole) {

    user = selectedRole.getAttribute('value')
    if (user == 'student') {
      url_b = "../static/images/student.png";
      document.body.style.backgroundImage = 'url(' + url_b + ')';
    }
    else if (user == 'teacher') {
      url_b = "../static/images/student_login.png";

      document.body.style.backgroundImage = 'url(' + url_b + ')';
    }
    else if (user == 'it_staff') {
      url_b = "../static/images/it_staff.jpeg";
      document.body.style.backgroundImage = 'url(' + url_b + ')';
    }
    else if (user == 'admin') {
      url_b = "../static/images/admin_cartoon.jpeg";
      document.body.style.backgroundImage = 'url(' + url_b + ')';
    }

  } else {
    console.log('No image selected');
  }
}, 1000);

