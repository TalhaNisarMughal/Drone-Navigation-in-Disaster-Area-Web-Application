let allShapeCoordinates = [];
function openNav() {
    document.getElementById("mySidenav").style.width = "340px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById('open').style.display = 'none'
  }
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById('open').style.display = 'inline'
  }
// Show Map
mapboxgl.accessToken = 'pk.eyJ1Ijoid2FxYXJtdW4iLCJhIjoiY2xmNnB0MnZ3MHhjMjN5cWh3YWtnMHZsMyJ9.DdA5uGyoRwdIZp9u0hK-SA';
const map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/satellite-streets-v12', 
center: [74.24076031193948, 31.39222922632956],
zoom: 15 // 
});
// End Show map
map.addControl(new mapboxgl.NavigationControl());
 draw = new MapboxDraw({
displayControlsDefault: false,
controls: {
polygon: true,
trash: true
},
});
map.addControl(draw);
map.on('draw.create', updateArea);
map.on('draw.delete', updateArea);
map.on('draw.update', updateArea);
map.addControl(
new mapboxgl.GeolocateControl({
positionOptions: {
enableHighAccuracy: true
},
trackUserLocation: true,
showUserHeading: true
})
);
//  marker = new mapboxgl.Marker({
// draggable: false
// })
// .setLngLat([74.24076031193948, 31.39222922632956])
// .addTo(map);
// function onDragEnd() {
// const lngLat = marker.getLngLat();
// function cordin(lngLat){
//     return lngLat
// }
// var start = [lngLat.lng,lngLat.lat]
// }
// marker.on('dragend', onDragEnd);
function updateArea(e) {
const data = draw.getAll();
cor=data['features'][0]['geometry']['coordinates'];
console.log(cor)
allShapeCoordinates.push(cor)
console.log(allShapeCoordinates)
if (data.features.length > 0) {
const area = turf.area(data);
const rounded_area = Math.round(area * 100) / 100;
} else {
answer.innerHTML = '';
if (e.type !== 'draw.delete')
alert('Click the map to draw a polygon.');
}
var overlaping_rate = document.getElementById('overlap').value
var Aspect_Ration = document.getElementById("asra").value
var Altitude = document.getElementById("flight-altitude").value
var Algo = document.getElementById("Algo").value
var nfz = document.getElementById("flexSwitchCheckChecked").checked
if (nfz){
  const lastElement = allShapeCoordinates[allShapeCoordinates.length - 1];
  const secondLastElement = allShapeCoordinates[allShapeCoordinates.length - 2];
  var data2 = {'cordinates':secondLastElement,"overlaping":overlaping_rate,"ar":Aspect_Ration,"height":Altitude,"Algo":Algo,"NFZ":lastElement}
  var csrfToken = document.getElementById('csrf_token').value;
 $.ajax({
     type: 'POST',
     url: 'ppNFZ/',
     data: data2,
     headers: {'X-CSRFToken': csrfToken}, 
     success: function(data1) {
var path_geojson_obj = JSON.parse(data1);
if (map.getLayer('path')) {
    map.removeLayer('path');
}
if (map.getSource('path')) {
    map.removeSource('path');
}
map.addSource('path', {
    type: 'geojson',
    data: path_geojson_obj
});
map.addLayer({
    id: 'path',
    type: 'line',
    source: 'path',
    layout: {},
    paint: {
        'line-color': '#FF0000',
        'line-width': 1
    }
});
     },
     error: function(xhr, textStatus, errorThrown) {
         console.log('Error sending data: ' + errorThrown);
     }
 });
}
else{
    const lastElement = allShapeCoordinates[allShapeCoordinates.length - 1];
    // const secondLastElement = array[array.length - 2];
    cor2=data['features'][0]['geometry']['coordinates'];
    var previous_cord = cor2
    var data2 = {'cordinates':lastElement,"overlaping":overlaping_rate,"ar":Aspect_Ration,"height":Altitude,"Algo":Algo}
    var csrfToken = document.getElementById('csrf_token').value;
   $.ajax({
       type: 'POST',
       url: 'pp/',
       data: data2,
       headers: {'X-CSRFToken': csrfToken}, 
       success: function(data1) {
  var path_geojson_obj = JSON.parse(data1);
  if (map.getLayer('path')) {
      map.removeLayer('path');
  }
  if (map.getSource('path')) {
      map.removeSource('path');
  }
  map.addSource('path', {
      type: 'geojson',
      data: path_geojson_obj
  });
  map.addLayer({
      id: 'path',
      type: 'line',
      source: 'path',
      layout: {},
      paint: {
          'line-color': '#FF0000',
          'line-width': 1
      }
  });
       },
       error: function(xhr, textStatus, errorThrown) {
           console.log('Error sending data: ' + errorThrown);
       }
   });
}
}