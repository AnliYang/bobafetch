function initMap() {

// specifying map center
var myLatLng = {lat: 37.7898750430312, lng: -122.407143359783};

// map object with DOM element for display
var map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    zoom: 15,
});

}

// listener for the DOM
google.maps.event.addDomListener(window, 'load', initMap);
