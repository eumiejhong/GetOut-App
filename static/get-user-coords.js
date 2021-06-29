var x = document.getElementById("coords");

function gotLocationFromUser(position) {
  var x = document.getElementById("coords");
  x.innerHTML = "Latitude: " + position.coords.latitude +
  "<br>Longitude: " + position.coords.longitude;

  $('input[name="lat"]').val(position.coords.latitude);
  $('input[name="long"]').val(position.coords.longitude);

  if (window.map) {
    const ll = new L.LatLng(position.coords.latitude, position.coords.longitude)
    window.map.panTo(ll);
  }
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(gotLocationFromUser);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

$(function(){
  $("#coord-btn").click(getLocation);
});


