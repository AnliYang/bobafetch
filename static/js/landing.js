    var userLat = document.getElementById("latitude");
var userLng = document.getElementById("longitude");
var userAddress = document.getElementById("address");
var progressBar = document.getElementById("progress")

function getLocation() {
    showLoading();
    navigator.geolocation.getCurrentPosition(setPosition);
}

function showLoading() {
    // userLat.placeholder = 'fetching...';
    // userLng.placeholder = 'fetching...';
    progressBar.classList.remove('hidden');
}

function setPosition(position) {
    userAddress.placeholder = "latitude: " + position.coords.latitude.toPrecision(6) + ", longitude: " + position.coords.longitude.toPrecision(7);
    // var userLat = document.getElementById("latitude");
    userLat.value = position.coords.latitude;

    // var userLng = document.getElementById("longitude");
    userLng.value = position.coords.longitude;

    progressBar.classList.add('hidden');
}

var geolocate = document.getElementById('geolocate');

geolocate.addEventListener('click', getLocation);