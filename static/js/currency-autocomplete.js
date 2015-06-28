$(function () {
    // setup autocomplete function pulling from currencies[] array
    $("#autocomplete").autocomplete({
        delay: 500,
        source: function (request, response) {
            $.getJSON("/action/query", {
                queryString: request.term,
                page_limit: 20
            }, function (data) {
                // data is an array of objects and must be transformed for autocomplete to use
                var array = data.data.length == 0 ? [] : $.map(data.data[0].fields, function (m) {
                    return {
                        label: m['value'],
                        url: null
                    };
                });
                response(array);
            });
        },
        focus: function (event, ui) {
            // prevent autocomplete from updating the textbox
            event.preventDefault();
        },
        select: function (event, ui) {
            // prevent autocomplete from updating the textbox
            event.preventDefault();
            // navigate to the selected item's url
            codeAddress(ui.item.label);
        }
    });

});
$(document).ready(function () {
    // your code here
});

var geocoder;
var map;
function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-34.397, 150.644);
    var mapOptions = {
        zoom: 13,
        center: latlng
    }
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

function codeAddress(address) {
    //var address = document.getElementById('address').value;
    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                zoom: 13,
                position: results[0].geometry.location
            });
            // Construct the circle for each value in citymap.
            // Note: We scale the area of the circle based on the population.
            /*            var citymap = {};
             citymap['chicago'] = {
             center: new google.maps.LatLng(41.878113, -87.629798),
             population: 2714856
             };
             citymap['newyork'] = {
             center: new google.maps.LatLng(40.714352, -74.005973),
             population: 8405837
             };
             citymap['losangeles'] = {
             center: new google.maps.LatLng(34.052234, -118.243684),
             population: 3857799
             };
             citymap['vancouver'] = {
             center: new google.maps.LatLng(49.25, -123.1),
             population: 603502
             };*/

            var inner;
            var populationOptions = {
                strokeColor: '#00FF00',
                strokeOpacity: 0.8,
                strokeWeight: 3,
                fillColor: '#00FF00',
                fillOpacity: 0.35,
                map: map,
                center: results[0].geometry.location,
                radius: 1000
            };
            inner = new google.maps.Circle(populationOptions);

            var outer;
            var optionsOuter = {
                strokeColor: '#f6b6d6',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#f6b6d6',
                fillOpacity: 0.45,
                map: map,
                center: results[0].geometry.location,
                radius: 2000
            };
            outer = new google.maps.Circle(optionsOuter);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

google.maps.event.addDomListener(window, 'load', initialize);