// configs
var map = L.map("map").setView([40.519365, -3.894206], 14.2);
L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
  {
    attribution:
      'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken:
      "pk.eyJ1IjoianVhbmFsMDciLCJhIjoiY2wxZ3RjcWhlMDRqeDNmb2N0NmRocmJzbSJ9.P-pUIVGZXiJL01Bn9_rLSw",
  }
).addTo(map);

// routes
var colors = ["#cc241d", "#b16286", "#d79921"];
var i = 0;
fetch("../output/route_points.json")
  .then((response) => response.json())
  .then((jsondata) => {
    jsondata.map((route) => {
      L.polyline(route, { color: colors[i % 3] }).addTo(map);
      i++;
    });
  });

// cubos
var iconBasura = L.icon({
  iconUrl: "./img/cubo.png",
  iconSize: [20, 20],
});
fetch("../data/locations.json")
  .then((response) => response.json())
  .then((jsondata) => {
    jsondata.map((cubo) => {
      console.log(cubo);
      L.marker([cubo.lat, cubo.lng], { icon: iconBasura }).addTo(map);
    });
  });

// camiones
var iconCamion = L.icon({
  iconUrl: "./img/camion.png",
  iconSize: [40, 40],
});
fetch("../data/drivers.json")
  .then((response) => response.json())
  .then((jsondata) => {
    jsondata.map((c) => {
      console.log(c);
      L.marker([c.lat, c.lng], { icon: iconCamion }).addTo(map);
    });
  });

// hp
var iconHP = L.icon({
  iconUrl: "./img/hpe-logo.png",
  iconSize: [50, 40],
});
L.marker([40.516317, -3.895065], { icon: iconHP }).addTo(map);

// show coords onClick
var popup = L.popup();
function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
}
map.on("click", onMapClick);
