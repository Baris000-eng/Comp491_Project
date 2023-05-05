function changeBackgroundColor(color) {
  document.body.style.backgroundColor = color;
}

let imageIndex = 1;
	let selectedImage = document.querySelector(".image");
	let imagesList = ["../static/images/img1.png", "../static/images/img2.png", "../static/images/img3.png"];
	setInterval(() => {
		if (imageIndex + 1 > imagesList.length) {
			imageIndex = 0;
		}

		selectedImage.src = imagesList[imageIndex];
		imageIndex = imageIndex + 1;
	}, 1000);

	const form = document.querySelector('form');

