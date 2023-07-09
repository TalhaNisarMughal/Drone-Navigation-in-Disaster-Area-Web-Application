function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
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
zoom: 17 // 
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
cor=data['features'][0]['geometry']['coordinates'][0];
console.log(cor)
if (data.features.length > 0) {
const area = turf.area(data);
const rounded_area = Math.round(area * 100) / 100;
} else {
answer.innerHTML = '';
if (e.type !== 'draw.delete')
alert('Click the map to draw a polygon.');
}
var data2 = {'cordinates':cor}
 var csrftoken = getCookie('csrftoken');
 $.ajax({
     type: 'POST',
     url: 'pp/',
     data: data2,
     headers: {'X-CSRFToken': csrftoken}, 
     success: function(data1) {
var path_geojson_obj = JSON.parse(data1);
console.log(data1)
map.addSource('path', {
    type: 'geojson',
    data: path_geojson_obj
});

// Add a `line` layer to the map that uses the `path` data source
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
 function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = cookies[i].trim();
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }
}


