L.mapbox.accessToken = 'pk.eyJ1IjoiYW5saXlhbmciLCJhIjoiY2lvZ25wbTB4MDFrdHU3a212eGZwcW91NSJ9.GOtW72gefCHdD1Y-6bza-w';

var userLat = $('#map_geo').data('user-lat');
var userLng = $('#map_geo').data('user-lng');
var userAddress = $('#map_geo').data('user-address');
var userRunSpeed = $('#map_geo').data('run-speed');

var features = $('#map_geo').data('feature-collection')

var mapGeo = L.mapbox.map('map_geo', 'mapbox.dark')
    .setView([userLat, userLng], 13);

var featureLayer = L.mapbox.featureLayer();

function addMarkers(features) {
    featureLayer.setGeoJSON(features).addTo(mapGeo);
    mapGeo.scrollWheelZoom.disable();
}

addMarkers(features);

featureLayer.eachLayer(function(layer) {
    restaurant = layer.feature.properties
    var content =
        '<div class="caption">' +
        '<h1 align="center"><b>' + restaurant["name"] + '</b><\/h1>' +
        '<div align="center">' + restaurant["street1"] + '</div>' +
        '<div align="center">' + restaurant["city"] + ', ' + restaurant["state"] + ' ' + restaurant["zip"] + '</div>' +
        '<br \/>' +
        '<form action="/map" method="POST">' +
            '<input type="hidden" name="yelp-id" value="' + restaurant["yelp-location-id"] + '">' +
            '<input type="hidden" name="user-address" value="' + userAddress + '">' +
            '<input type="hidden" name="user-lat" value="' + userLat + '">' +
            '<input type="hidden" name="user-lng" value="' + userLng + '">' +
            '<input type="hidden" name="run-speed" value="' + userRunSpeed + '">' +
            '<button type="submit" class="btn btn-primary">' +
            '<span class="glyphicon glyphicon-map-marker" aria-hidden="true"></span>' +
            ' Map It!</button></form>' +
        '<br \/>' +
        '<a href="' + restaurant["url"] + '" class="btn btn-warning"><i class="fa fa-yelp"></i> Read reviews!' +
        '</div>'
        ;
    layer.bindPopup(content);
});
