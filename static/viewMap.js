var originalImageURL = '../static/images/map3d.png';
var sosImageURL = '../static/images/sos.png';
var caseImageURL = '../static/images/case.png';
var studentcenterURL = '../static/images/student_center.png';
var scienceURL = '../static/images/science.png';
var libraryURL = '../static/images/library.png';
var elcURL = '../static/images/elc.png';
var dormsURL = '../static/images/dorms.png';
var snaaURL = '../static/images/snaa.png';
var snabURL = '../static/images/snab.png';
var engURL = '../static/images/eng.png';


function changeImageURLSNA(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : dormsImageURL;
}
function changeImageURLSOS(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : sosImageURL;
}

function changeImageURLCASE(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : caseImageURL;
}

function changeImageURLSTUDENTCENTER(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : studentcenterURL;
}

function changeImageURLSCIENCE(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : scienceURL;
}
function changeImageURLLIBRARY(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : libraryURL;
}
function changeImageURLELC(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : elcURL;
}

function changeImageURLDORMS(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : dormsURL;
}

function changeImageURLSNAA(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : snaaURL;
}

function changeImageURLSNAB(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : snabURL;
}
function changeImageURLENG(isHovered) {
    var mapImage = document.getElementById('map-image');
    mapImage.src = isHovered ? originalImageURL : engURL;
}



