var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
// var map;

var mapElement = document.getElementById('map');

var endLatitude = parseFloat(mapElement.dataset.endlat);
var endLongitude = parseFloat(mapElement.dataset.endlng);
var endLatLng = {lat: endLatitude, lng: endLongitude};

var startAddress = mapElement.dataset.startaddress;

var startLatitude = parseFloat(mapElement.dataset.startlat);
var startLongitude = parseFloat(mapElement.dataset.startlng);
var startLatLng = {lat: startLatitude, lng: startLongitude};

function initialize() {
    directionsDisplay = new google.maps.DirectionsRenderer();
  
// no center, because gonna change to center on route anyway
    var mapOptions = {
        zoom:15,
    };
  
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById("directionsPanel"));
}

function calcRoute() {
    // var start = startAddress;
    var start;
    if (startAddress !== "") {
        start = startAddress;
    } else {
        start = startLatLng;
    }

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

// listener for the DOM
google.maps.event.addDomListener(window, 'load', showMap);


// function to calculate runtime with running speed
var runSpeed = mapElement.dataset.runspd;

// function to calculate total distance (Google distance * 2)
// var distance = ;


// for error case when no yelp results are returned
// function initPlainMap() {

//     var mapElement = document.getElementById('map');

//     var latitude = parseFloat(mapElement.dataset.lat);

//     var longitude = parseFloat(mapElement.dataset.lng);

//     // specifying map center
//     var myLatLng = {lat: latitude, lng: longitude};

//     // map object with DOM element for display
//     var map = new google.maps.Map(mapElement, {
//         center: myLatLng,
//         zoom: 15,
//         });

// }

// google.maps.event.addDomListener(window, 'load', initPlainMap);