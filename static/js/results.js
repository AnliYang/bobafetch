L.mapbox.accessToken = 'pk.eyJ1IjoiYW5saXlhbmciLCJhIjoiY2lvZ25wbTB4MDFrdHU3a212eGZwcW91NSJ9.GOtW72gefCHdD1Y-6bza-w';

// var restaurantIds = $('#map_geo').data('restaurant-ids');
// $.get('/restaurant-locations.geojson', {'restaurant-ids': restaurantIds}, addMarkers);

var userLat = $('#map_geo').data('user-lat');
var userLng = $('#map_geo').data('user-lng');
var features = $('#map_geo').data('feature-collection')

var mapGeo = L.mapbox.map('map_geo', 'mapbox.dark')
  .setView([userLat, userLng], 14);

function addMarkers(features) {
    L.mapbox.featureLayer().setGeoJSON(features).addTo(mapGeo);
    mapGeo.scrollWheelZoom.disable();
}

addMarkers(features);


// function addMarkers(results) {
//     L.mapbox.featureLayer().setGeoJSON(results).addTo(mapGeo);
//     mapGeo.scrollWheelZoom.disable();
// }

// var resultsElement = document.getElementById('results');
//
// var restaurants = resultsElement.dataset.restaurants;
// var range = resultsElement.dataset.range;
//
// var restaurantIds = $('#map_geo').data('restaurant-ids');
