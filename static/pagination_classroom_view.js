function showPage(pageNumber) {
  const images = document.querySelectorAll("#image-container img");
  const startingIndex = (pageNumber - 1) * 16;
  let endingIndex = startingIndex + 16;

  if (endingIndex > images.length) {
    endingIndex = images.length;
  }

  for (let i = 0; i < images.length; i++) {
    if (i >= startingIndex && i < endingIndex) {
      images[i].style.display = "block";
    } else {
      images[i].style.display = "none";
    }
  }
}

function redirectToReservationScreen(value, role) {
  var url = "";
  if (role == "student") {
    url = "/openStudentReservationScreen?value=" + value;
  } else if (role == "teacher") {
    url = "/openTeacherReservationScreen?value=" + value;
  } else if (role == "it_staff") {
    url = "/openITStaffReservationScreen?value=" + value;
  }

  location.href = url;
}
