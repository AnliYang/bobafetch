function getLocation() {
    navigator.geolocation.getCurrentPosition(setPosition);
}

function setPosition(position) {
    var userLat = document.getElementById("latitude");
    userLat.value = position.coords.latitude;

    var userLng = document.getElementById("longitude");
    userLng.value = position.coords.longitude;
}

var geolocate = document.getElementById('geolocate');

geolocate.addEventListener('click', getLocation);