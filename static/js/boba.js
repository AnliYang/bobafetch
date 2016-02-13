function initMap() {

var mapElement = document.getElementById('map');

var latitude = parseFloat(mapElement.dataset.lat);

var longitude = parseFloat(mapElement.dataset.lng);

// specifying map center
var myLatLng = {lat: latitude, lng: longitude};

// map object with DOM element for display
var map = new google.maps.Map(mapElement, {
    center: myLatLng,
    zoom: 15,
});

}

// listener for the DOM
google.maps.event.addDomListener(window, 'load', initMap);
