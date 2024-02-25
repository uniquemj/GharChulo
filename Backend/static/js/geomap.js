let map;
let marker;
let markerPlacementEnabled = false;

function enableMarkerPlacement() {
    markerPlacementEnabled = true;
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 27.7172, lng: 85.3240 },
        zoom: 15
    });
    
    map.addListener('click', function(event) {
            console.log(event.latLng)
            placeMarker(event.latLng);
            reverseGeocode(event.latLng);

    });
}

function placeMarker(location) {
    if (!marker) {
        marker = new google.maps.Marker({
            position: location,
            map: map,
            draggable: true
        });

        marker.addListener('dragend', function(event) {
            reverseGeocode(event.latLng);
        });
    } else {
        marker.setPosition(location);
    }
}

function reverseGeocode(location) {
    let geocoder = new google.maps.Geocoder();

    geocoder.geocode({ 'location': location }, function(results, status) {
        if (status === 'OK') {
            if (results[0]) {
                let address = results[0].formatted_address;
                let latitude = location.lat();
                let longitude = location.lng();
                let saveBtn = document.getElementById('save')
                saveBtn.addEventListener('click',() => {
                    getLocation(address, latitude, longitude)
                })
            }
        } else {
            alert('Geocoder failed due to: ' + status);
        }
    });
}


const getLocation = (location, lat, lng) => {
    url = "/settings/";
    console.log(lat)
    $.ajax({
        type: "POST",
        url: url,
        headers: {
            "X-CSRFToken": csrftoken,
        },
        data: {
            location: location,
            lat: lat,
            lng: lng
        },
        dataType: "json",
        success: function (data) {
            console.log("data: ", data);
        },
        failure: function () {
            console.log("Location fetch fail Failed");
        },
    });
};

initMap();