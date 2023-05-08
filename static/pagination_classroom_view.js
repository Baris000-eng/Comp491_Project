function showPage(pageNumber) {
  const images = document.querySelectorAll("#image-container img");
  const startingIndex = (pageNumber - 1) * 9;
  let endingIndex = startingIndex + 9;

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

