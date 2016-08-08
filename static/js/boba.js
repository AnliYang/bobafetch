// FAVORITES AND VISITED RESTAURANTS
$(window).load(checkForLoggedIn);
$('#favorite').click(addToFavorites);
$('#visited').click(addToVisited);

function checkForLoggedIn(evt){
    var loggedIn;
    $.get("/check-for-logged-in", loggedInSuccess);
    // returning loggedIn isn't working here because of async; the function for checkForLoggedIn completes before the sucess function finishes
}

function loggedInSuccess(result){
    if (result.status === "logged-in") {
        console.log("logged-in")
        checkForFavorite();
        checkForVisited();
        loggedIn = true;
    } else {
        console.log("logged-out")
        loggedIn = false;
    }
}

function checkForFavorite(evt){
    console.log("checking for favorites")
    var favoriteButton = $('#favorite');
    var yelpId = favoriteButton.attr('name');
    $.get("/check-for-favorite", {'yelp-id': yelpId}, FavoritesSuccess);
}

function addToFavorites(evt){
    var yelpId = this.name;
    $.post("/add-to-favorites", {'yelp-id': yelpId}, FavoritesSuccess);
}

function FavoritesSuccess(result){
    if (result.status === 'favorite') {
        console.log(result.status);
        // var yelpId = result.id;
        $('#favorite').addClass('active');
        $('.btn-favorite').removeClass('btn-default').addClass('btn-danger')
        $('.favorite-heart').removeClass('fa-heart-o').addClass('fa-heart') // give our user some feedback
    } else if (result.status === 'not-favorite') {
    } else {
        $('#login-please').removeAttr('hidden');
    }
}

function checkForVisited(evt){
    var yelpId = $('#visited').attr('name');
    $.get("/check-for-visited", {'yelp-id': yelpId}, VisitedSuccess);
}

function addToVisited(evt){
    var yelpId = this.name;
    $.post("/add-to-visited", {'yelp-id': yelpId}, VisitedSuccess);
}

function VisitedSuccess(result){
    if (result.status === 'visited') {
        console.log(result.status);
        // var yelpId = result.id;
        $('#visited').addClass('active');
        $('.btn-visited').removeClass('btn-default').addClass('btn-success');
        $('.visited-flag').removeClass('fa-flag').addClass('fa-flag-checkered'); // give our user some feedback
    } else if (result.status === 'not-visited') {
    } else {
        $('#login-please').removeAttr('hidden');
    }
}


// GOOGLE DIRECTIONS/MAP STUFF
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();

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

// calculate runtime with running speed
var runSpeed = mapElement.dataset.runspd;


// BACK BUTTON
function goBack() {
    window.history.back();
}
