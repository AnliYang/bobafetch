// jquery shortcut for document.ready()
$(function (){
    function checkForFavorite(evt){
        var favoriteButton = $('#favorite');
        var yelpId = favoriteButton.attr('name');
        $.post("/check-for-favorite", {'yelp-id': yelpId}, FavoritesSuccess);
    }

    function addToFavorites(evt){
        var yelpId = this.name;
        $.post("/add-to-favorites", {'yelp-id': yelpId}, FavoritesSuccess);
    }

    function FavoritesSuccess(result){
        if (result.status === 'success') {
            console.log(result.status);
            // var yelpId = result.id;
            $('#favorite').addClass('active');
            $('.btn-favorite').removeClass('btn-default').addClass('btn-danger')
            $('.favorite-heart').removeClass('fa-heart-o').addClass('fa-heart') // give our user some feedback
        }
    }

    $(window).load(checkForFavorite);
    $('#favorite').click(addToFavorites);
});

$(function (){
    function checkForVisited(evt){
        var yelpId = $('#visited').attr('name');
        $.post("/checkForVisited", {'yelp-id': yelpId}, VisitedSuccess);
    }

    function addToVisited(evt){
        var yelpId = this.name;
        $.post("/add-to-visited", {'yelp-id': yelpId}, VisitedSuccess);
    }

    function VisitedSuccess(result){
        if (result.status === 'success') {
            console.log(result.status);
            // var yelpId = result.id;
            $('#visited').addClass('active');
            $('.btn-visited').removeClass('btn-default').addClass('btn-success');
            $('.visited-flag').removeClass('fa-flag').addClass('fa-flag-checkered'); // give our user some feedback
        }
    }

    $(window).load(checkForVisited);
    $('#visited').click(addToVisited);
});


// GOOGLE DIRECTIONS/MAP STUFF BELOW

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
            var warnings = document.getElementById("warnings-panel");
            warnings.innerHTML = "Warning: " + response.routes[0].warnings + "";
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
