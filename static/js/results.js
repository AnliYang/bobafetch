L.mapbox.accessToken = 'pk.eyJ1IjoiYW5saXlhbmciLCJhIjoiY2lvZ25wbTB4MDFrdHU3a212eGZwcW91NSJ9.GOtW72gefCHdD1Y-6bza-w';

var mapViewResults = $('#map-view-results');
var listViewResults = $('#list-view-results');

var userLat = mapViewResults.data('user-lat');
var userLng = mapViewResults.data('user-lng');
var userRunSpeed = mapViewResults.data('run-speed');

var features = mapViewResults.data('feature-collection')

var mapGeo = L.mapbox.map('map-view-results', 'mapbox.dark')
    .setView([userLat, userLng], 14);

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

var mapViewButton = $('#map-view-button');
var listViewButton = $('#list-view-button');

function toggleMap (evt) {
    console.log("Got into toggleMap!");
    mapViewResults.toggle();
    listViewResults.toggle();

// FIXME THIS IS A MESS
    if (mapViewButton.attr('disabled') === 'disabled') {
        mapViewButton.removeAttr('disabled');
        listViewButton.attr('disabled', 'disabled')
    }
    else {
        mapViewButton.attr('disabled', 'disabled')
        listViewButton.removeAttr('disabled');
    }

}

mapViewButton.click(toggleMap);
listViewButton.click(toggleMap);
