//Initialize the map
var map = new L.Map('map', {
  zoom: 6,
  minZoom: 3,
});

//Create a new tile layer
var tileUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
layer = new L.TileLayer(tileUrl,
{
    attribution: 'Maps © <a href=\"www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors',
    maxZoom: 18
});

//Add the layer to the map
map.addLayer(layer);

var locations = [
        [22.746593, 75.892373],
        [22.716271, 75.863647],
        [22.71219, 75.838767],
        [22.68287, 75.841188],
        [22.670965, 75.826809],
        [22.662245, 75.82688],
        [22.676855, 75.872163],
        [22.685871, 75.863019],
        [22.689655, 75.867503],
        [22.746593, 75.892373]
];

map.fitBounds(locations);

//Working with json file
let requestURL = 'file:///Users/mac/Desktop/major/orders.json';
let request = new XMLHttpRequest();
request.open('GET', requestURL);
request.responseType = 'json';
request.send();
request.onload = function() {
  const ordersJson = request.response;
}

//Marking the locations
var main_marker_icon = L.icon({
        iconUrl: 'file:///Users/aloy/Desktop/major/icons and images/main_marker.png',
        iconSize: [44, 48]
        });
var main_marker = L.marker(locations[0], {icon : main_marker_icon}).addTo(map).bindPopup("<b>Main</b><br>Dewas Naka");
var address_marker = L.marker(locations[1]).addTo(map).bindPopup("<b>Kummo</b><br>Jawahar Marg");
var address_marker = L.marker(locations[2]).addTo(map).bindPopup("<b>Allvin</b><br>MOG Line Road");
var address_marker = L.marker(locations[3]).addTo(map).bindPopup("<b>Aloysius</b><br>Kesar Bagh Road");
var address_marker = L.marker(locations[4]).addTo(map).bindPopup("<b>Rano</b><br>Rajendra Nagar");
var address_marker = L.marker(locations[5]).addTo(map).bindPopup("<b>Arnavi</b><br>Reti Mandi");
var address_marker = L.marker(locations[6]).addTo(map).bindPopup("<b>Chamanjot</b><br>Bholaram");
var address_marker = L.marker(locations[7]).addTo(map).bindPopup("<b>Dabbi</b><br>Bholaram");
var address_marker = L.marker(locations[8]).addTo(map).bindPopup("<b>Harfu</b><br>Indrapuri");

//Moving icon
var delivery_icon = L.icon({
        iconUrl: 'file:///Users/aloy/Desktop/major/icons and images/delivery_icon.png',
        iconSize: [40, 40]
        });
var x;
var speed = [];
var seconds = 2000;
for(x=1; x<locations.length; x++){
        speed.push(seconds)
}
L.Marker.movingMarker(locations, speed, {autostart: true, loop: true, icon : delivery_icon}).addTo(map);

//Adding lines between the locations
L.polyline(locations, {opacity: 1, weight: 3}).addTo(map);
