let lat, lng
if ("geolocation" in navigator) {
    // Geolocation is available
    navigator.geolocation.getCurrentPosition(function(position) {
        lat = position.coords.latitude;
        lng = position.coords.longitude;
        currentPosition(lat, lng)
    });
} else {
    // Geolocation is not available in this browser
    console.log("Geolocation is not supported.");
}

function currentPosition(lat, lng){
    console.log(lat, lng)
    url = '/'
    $.ajax({
    type: "POST",
    url: url,
    headers: {
        "X-CSRFToken": csrftoken,
    },
    data: {
        currentLatitude: lat,
        currentLongitude: lng
    },
    dataType: "json",
    success: function (data) {
        console.log("data: ", data);
    },
    failure: function () {
      console.log("Location Tracking Failed.");
    },
    });
}