function fetchData(pageNumber, pageSize) {
    return $.ajax({
        url: '/data',
        method: 'GET',
        data: {
            page: pageNumber,
            size: pageSize
        }
    });
}

// Function to add markers to the map
function addMarkers(data) {
    // Add markers to the map based on the fetched data
    data.forEach(function(point) {
        var marker = L.marker([point[0], point[1]]).addTo(map);
        // Customize marker as needed
    });
}

// Event listener for map movement or zoom change
map.on('moveend', function() {
    var bounds = map.getBounds();
    var zoomLevel = map.getZoom();
    var pageNumber = 1; // Adjust this based on your pagination logic
    var pageSize = 1000; // Adjust the page size based on performance

    // Fetch data from the server based on the current map view
    fetchData(pageNumber, pageSize)
        .done(function(data) {
            // Add markers to the map
            addMarkers(data);
        })
        .fail(function(error) {
            console.error('Error fetching data:', error);
        });
});