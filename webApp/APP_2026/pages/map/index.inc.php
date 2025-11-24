<!-- Import Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
     integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
     crossorigin=""/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />

<!-- Import Leaflet JS -->
 <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
     integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
     crossorigin="">
</script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

<!-- Map component -->
<div id="map" style="height: calc(100vh - 80px); width: 100%;"></div>

<!-- Fetch univ list from DB -->
<?php 
    $sql = "SELECT * FROM MOB_partner_university";
    $result = mysqli_query($conn, $sql) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql);
    $universities = mysqli_fetch_all($result, MYSQLI_ASSOC);
?>

<script>
    var map = L.map('map').setView([48.85, 2.35], 4);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var markers = L.markerClusterGroup();
    var universities = <?= json_encode($universities) ?>;
    universities.forEach(function(university) {
        var marker = L.marker([university.latitude, university.longitude])
            .bindPopup('<b>' + university.name + '</b><br>' + university.address + ', ' + university.country);
        markers.addLayer(marker);
    });
    map.addLayer(markers);
</script>