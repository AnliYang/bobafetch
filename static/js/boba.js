var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
// var map;

var mapElement = document.getElementById('map');

var endLatitude = parseFloat(mapElement.dataset.endlat);
var endLongitude = parseFloat(mapElement.dataset.endlng);
var endLatLng = {lat: endLatitude, lng: endLongitude};

var startAddress = mapElement.dataset.startaddress;

function initialize() {
    directionsDisplay = new google.maps.DirectionsRenderer();
  
// QUESTION: do I need to have a center?
    var mapOptions = {
        zoom:15,
    // center: endLatLng
    };
  
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById("directionsPanel"));
}

function calcRoute() {
    var start = startAddress;

    var end = endLatLng;
    var request = {
        origin:start,
        destination:end,
        travelMode: google.maps.TravelMode.WALKING
    };
  
    var directionsService = new google.maps.DirectionsService();

    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });
}

function showMap() {
    initialize();
    calcRoute();
}

google.maps.event.addDomListener(window, 'load', showMap);