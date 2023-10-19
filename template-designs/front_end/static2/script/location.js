/**
 * The following code uses the Haversine formula for calculating the distance
 * between the user and the targeted hospital.
 *
 * The haversine formula determines the great-circle distance between two points
 * on a sphere given their longitudes and latitudes. The formula calcultates the
 * distance between two points on a sphere as the crow flies (straight-line distance).
 *
 * The result from the following calculation doesn't comply with the actual driving
 * distance between two points. The result will be the shortest distance between user's
 * location and the target hospital.
 */

$(function () {
  // Get the id of the hospital object
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get('id');

  let hospitalLatitude = 0;
  let hospitalLongitude = 0;

  // Make a get request to retrive the required hospital object.
  $.ajax({
    type: 'GET',
    url: `http://0.0.0.0:5001/api/v1/hospitals/${id}`,
    contentType: 'application/json',
    success: function (response) {
      hospitalLatitude = response.lattitude;
      hospitalLongitude = response.longitude;
    },
  });
  // A  function that calculates the distance between two points using
  // Latitude and Longitude
  function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const d = R * c;
    if (d > 1) return d.toFixed(3) + 'km';
    else if (d <= 1) return Math.round(d * 1000) + 'm';
    return d;
  }
  $('button#btn-see-distance').click(function () {
    computeDistance();
  });

  // Function for computing the distance between two points
  function computeDistance() {
    // Check if the geolocatio API is supported by the browser
    if (navigator.geolocation) {
      // Get the current postion
      navigator.geolocation.getCurrentPosition(getLocation);
    } else {
      console.log('Geolocation is not supported by this browser.');
    }

    // Function that gets the required latitude and longitude values
    function getLocation(position) {
      latitude = position.coords.latitude;
      longitude = position.coords.longitude;
      const distance = calculateDistance(
        latitude,
        longitude,
        hospitalLatitude,
        hospitalLongitude,
      );
      $('#show-distance').text(distance);
    }
  }
});
