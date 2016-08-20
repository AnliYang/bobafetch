L.mapbox.accessToken = 'pk.eyJ1IjoiYW5saXlhbmciLCJhIjoiY2lvZ25wbTB4MDFrdHU3a212eGZwcW91NSJ9.GOtW72gefCHdD1Y-6bza-w';

var userLat = $('#map_geo').data('user-lat');
var userLng = $('#map_geo').data('user-lng');
var features = $('#map_geo').data('feature-collection')

var mapGeo = L.mapbox.map('map_geo', 'mapbox.dark')
  .setView([userLat, userLng], 15);

function addMarkers(features) {
    L.mapbox.featureLayer().setGeoJSON(features).addTo(mapGeo);
    mapGeo.scrollWheelZoom.disable();
}

addMarkers(features);
