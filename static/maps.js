$(function(){

  const markers = [];
  window.map = null;

  function initMap(data) {
    if (map) {
      return;
    }

    let latitude = data.params.latitude;
    //console.log(latitude)
    let longitude = data.params.longitude;
    //console.log(longitude)
    map = L.map('mapid').setView([latitude, longitude], 10);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'pk.eyJ1IjoiZXVtaWVqaG9uZyIsImEiOiJja3E2cWFyZGMwNnBzMnJsZndvbndpdnRtIn0.6K4b-FpA_YY0_yVFOvxL6g'
      }).addTo(map);
  }

  function startWatchingMove() {
    map.on('dragend', function(e){
      let {lat, lng} = map.getCenter();
      requestNewDataAndRender($('#radius').val() || 25, lat, lng);
    })
  }

  function makeMarker(site) {
    let marker = L.marker([site.latitude, site.longitude]).addTo(map);
    marker.bindPopup(generateSiteMarkerHTML(site));
    markers.push(marker);
  }

  // Render the map
  function renderMarkers(data) {
    clearMarkers();

    for(let campsite of data.campsites) {
      makeMarker(campsite);
    }

    for(let rec_park of data.rec_parks) {
      makeMarker(rec_park);
    }
  }

  function clearMarkers () {
    for (let marker of markers){
      marker.remove();
    }
  }

  async function requestNewDataAndRender(radius, lat, long){
    const response = await axios.get('/api', {params: {radius, lat, long}});

    if (response.data) {
      renderMarkers(response.data);
    }
  }
  
  // Runs on page load
  initMap(window.pageData);
  renderMarkers(window.pageData);
  startWatchingMove();

  $('#radius-form').on('submit', async function(e){
    e.preventDefault();

    const radius = $('#radius').val();
    const lat = $('#lat-camp').val();
    const long = $('#long-camp').val();

    await requestNewDataAndRender(radius, lat, long);
  })
});


function renderLikeButton(site, objectType) {
  return `<div class="d-inline like-btn" data-type="${objectType}" data-object-id="${site.id}" data-liked="${site.has_liked}">
  <i class="${site.has_liked ? 'fas' : 'far'} fa-heart fa-2x"></i>
</div>`
}


function generateSiteMarkerHTML(site, objectType) {
  objectType = site.type;
  link = `/site/${site.id}/site-stories`
  return `
    <div class="card">
      <img class="card-img-top img-fluid img-thumbnail" src="${site.image_url}" alt="Card image cap">
      <div class="card-body">
        <h5 class="card-title">${site.name}</h5>
        <p class="card-text">${site.directions}</p>
        ${renderLikeButton(site, objectType)}
        <a href=${link} class="btn btn-sm btn-success" id="stories-button">Stories</a>
      </div>
    </div>
  `
}

