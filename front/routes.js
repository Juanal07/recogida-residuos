var map = L.map("map").setView([40.519365, -3.894206], 14.5);
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

var latlngs;

latlngs = [
  [40.519163, -3.887558],
  [40.5187906, -3.886666599999999],
  [40.5177208, -3.8854349],
  [40.5151532, -3.8834905],
  [40.5106955, -3.8918934],
  [40.5130758, -3.8944415],
  [40.5138218, -3.8957329],
  [40.5160103, -3.899899199999999],
  [40.5183433, -3.8972776],
  [40.518348, -3.897235],
  [40.518348, -3.897235],
  [40.5207997, -3.8959846],
  [40.520794, -3.896012],
  [40.520794, -3.896012],
  [40.52201489999999, -3.893562899999999],
  [40.5224543, -3.8943081],
  [40.5224249, -3.8943379],
  [40.522425, -3.894338],
  [40.522425, -3.894338],
  [40.5207997, -3.8959846],
  [40.517827, -3.8915637],
  [40.5185579, -3.8921628],
  [40.5186947, -3.8920234],
  [40.51871149999999, -3.8911092],
  [40.5192145, -3.8918196],
  [40.519228, -3.891806],
  [40.519228, -3.891806],
  [40.5196474, -3.892696399999999],
  [40.5187238, -3.8920719],
  [40.5185891, -3.8922105],
  [40.5193134, -3.8934653],
  [40.5209699, -3.8917907],
  [40.519715, -3.8896741],
  [40.5179857, -3.8912969],
  [40.5187376, -3.8894152],
  [40.5191782, -3.8875537],
  [40.519163, -3.887558],
];

var polyline = L.polyline(latlngs, { color: "red" }).addTo(map);

latlngs = [
  [40.526405, -3.893652],
  [40.5262922, -3.8936398],
  [40.526291, -3.893652],
  [40.526291, -3.893652],
  [40.5235689, -3.8931831],
  [40.523683, -3.8926009],
  [40.523681, -3.892622],
  [40.523681, -3.892622],
  [40.5250275, -3.8928272],
  [40.5235689, -3.8931831],
  [40.5235652, -3.8903521],
  [40.523535, -3.890347],
  [40.523535, -3.890347],
  [40.523367, -3.8923687],
  [40.5264046, -3.8936573],
  [40.526405, -3.893652],
];

var polyline3 = L.polyline(latlngs, { color: "blue" }).addTo(map);

latlngs = [
  [40.520566, -3.909616],
  [40.5193482, -3.9056934],
  [40.5213932, -3.901585],
  [40.5196868, -3.9005021],
  [40.519669, -3.900518],
  [40.519669, -3.900518],
  [40.5185441, -3.9041888],
  [40.5190559, -3.9052274],
  [40.5206091, -3.9095896],
  [40.520566, -3.909616],
];

var polyline3 = L.polyline(latlngs, { color: "yellow" }).addTo(map);

var marker = L.marker([40.520566, -3.909616]).addTo(map);
marker.bindPopup("<b>Hola!</b><br>Soy un camionero.");

var marker2 = L.marker([40.526405, -3.893652]).addTo(map);
marker2.bindPopup("<b>Hola!</b><br>Soy un camionero.");

var marker3 = L.marker([40.519163, -3.887558]).addTo(map);
marker3.bindPopup("<b>Hola!</b><br>Soy un camionero.");

// map.fitBounds(polyline.getBounds());
//
var popup = L.popup();

function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
}

map.on("click", onMapClick);
