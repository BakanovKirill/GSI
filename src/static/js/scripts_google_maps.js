var map;
var coord = [];
var markers = [];
var polygons = [];
var start_area = {lat: 0, lng: 0 };


function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 3,
    center: start_area
  });

  map.addListener('click', function(e) {
    placeMarkerAndPanTo(e.latLng.lat(), e.latLng.lng());
  });
}

function placeMarkerAndPanTo(lat1, lng1) {
  var dict = {
        'lat':   lat1,
        'lng': lng1
    }
  coord.push(dict);

  var marker = new google.maps.Marker({
    position: dict,
    map: map
  });
  //marker.setMap(map);
  //map.panTo(marker);
  markers.push(marker);
}

// Removes the poligon from the map, but keeps them in the array.
function removePoligon() {
  if (polygons) {
    for (i in polygons) {
      polygons[i].setMap(null);
    }
  }
  coord = [];
}

// Removes the markers from the map, but keeps them in the array.
function removeMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
}

function drawPoligon() {
  // Construct the polygon.
  var selectPolygon = new google.maps.Polygon({
    paths: coord,
    //strokeColor: '#FF0000',
    //strokeOpacity: 0.8,
    //strokeWeight: 3,
    fillColor: '#FF0000',
    fillOpacity: 0.3,
    //editable: true
  });
  selectPolygon.setMap(map);
  polygons.push(selectPolygon);
}

function toggleImageOverlays(){
  if (imgOverlaysVisible){
    for (i in overlays) overlays[i].setMap(null);
    imgOverlaysVisible = false;
  } else {
    //for (i in overlays) overlays[i].setMap(map_1);
    for (i in overlays){
      if (i!=cycleImg){
        overlays[i].setMap(null);
      } else {
        overlays[i].setMap(map_1);
      }
      imgOverlaysVisible = true;
   }
 }
}

function displayLatLng(){
  var x = 100;
  var y = 100;
  var pixel = 123; //ctx.getImageData(x, y, 1, 1).data;
  var contentString;

  var lat = document.getElementById('latitude');
  var lon = document.getElementById('longitude');
  var latlon;

  if (lat != 0)
     latlon = new google.maps.LatLng(lat, lon);
  else
     latlon = new google.maps.LatLng((minlat+maxlat)/2, (minlon+maxlon)/2);
  var MMmarker = null;

  var xsize = 520;
  var ysize = 760;

  google.maps.event.addListener(groundOverlay, 'mousemove', function (event)
  {
    alert('mousemove');
  	var lat = event.latLng.lat();
  	var lon = event.latLng.lng();
    xpos = xsize*(lon - minlon)/(maxlon-minlon);
    if (xpos<0) xpos=0;
    if (xpos>=xsize) xpos=xsize-1;
    ypos = ysize*(maxlat - lat)/(maxlat-minlat);
    if (ypos<0) ypos=0;
    if (ypos>=ysize) ypos=ysize-1;
    document.getElementById('latitude').value = lat.toFixed(6);
    document.getElementById('longitude').value = lon.toFixed(6);
  });

  var infowindow = new google.maps.InfoWindow();
  var x = null;

  google.maps.event.addListener(groundOverlay, 'click', function (event) {
  	var lat = event.latLng.lat();
  	var lon = event.latLng.lng();
    xpos = xsize*(lon - minlon)/(maxlon-minlon);
    if (xpos<0) xpos=0;
    if (xpos>=xsize) xpos=xsize-1;
    ypos = ysize*(maxlat - lat)/(maxlat-minlat);
    if (ypos<0) ypos=0;
    if (ypos>=ysize) ypos=ysize-1;

    chart = 0;
    if (document.getElementById('chart').value != null)
    {
       chart = document.getElementById('chart').value;
    }

    var fileName = document.getElementById('param').value + '.tif';
    if (document.getElementById('multifile').value != null)
    {
       if (document.getElementById('multifile').value.length>1)
       {
          fileName = document.getElementById('multifile').value + ".tif";
       }
       else
          chart = 0;
    }
    else
       chart = 0;
  });
}


$(document).ready(function(){
    // initMap();
    displayLatLng();
});
