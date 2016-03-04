var userLat = document.getElementById("latitude");
var userLng = document.getElementById("longitude");

function getLocation() {
    showLoading()
    navigator.geolocation.getCurrentPosition(setPosition);
}

function showLoading() {
    userLat.placeholder = 'loading...'
    userLng.placeholder = 'loading...'
}

function setPosition(position) {
    // var userLat = document.getElementById("latitude");
    userLat.value = position.coords.latitude;

    // var userLng = document.getElementById("longitude");
    userLng.value = position.coords.longitude;
}

var geolocate = document.getElementById('geolocate');

geolocate.addEventListener('click', getLocation);