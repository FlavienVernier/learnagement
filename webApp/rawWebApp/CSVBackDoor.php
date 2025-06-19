<?php

include("connectDB.php");

$vue = str_replace(" ", "_", $_GET["vue_name"]);

$req = "SELECT request FROM INFO_view WHERE name = '" . $_GET["vue_name"] ."'";
$result = mysqli_query($conn,$req);
while($row = mysqli_fetch_array($result)){
  $req = $row['request'];
}
//print($req);
// Fetch records from database 
$result = mysqli_query($conn,$req);
 
if($result){ 
    $delimiter = ","; 
    $filename = "data_" . $vue . "_" . date('Y-m-d') . ".csv"; 
    //$filename = "data_.csv"; 
    //print ($filename);
    // Create a file pointer 
    $f = fopen('php://memory', 'w'); 
     
    // Set column headers
    /*$fields = [];
    while ($row = mysqli_fetch_fields($result)){
      print($row);
      //array_push($fields, $row);
    }
    fputcsv($f, $fields, $delimiter);*/
    
     
    // Output each row of the data, format line as csv and write to file pointer 
    //while($row = $query->fetch_assoc()){ 
    while ($row = mysqli_fetch_row($result)) {
      //$status = ($row['status'] == 1)?'Active':'Inactive'; 
      //$lineData = array($row['id'], $row['first_name'], $row['last_name'], $row['email'], $row['gender'], $row['country'], $row['created'], $status);
      $lineData = $row;
        fputcsv($f, $lineData, $delimiter); 
    } 
     
    // Move back to beginning of file 
    fseek($f, 0); 
     
    // Set headers to download file rather than displayed 
    header('Content-Type: text/csv'); 
    header('Content-Disposition: attachment; filename="' . $filename . '";'); 
     
    //output all remaining data on a file pointer 
    fpassthru($f); 
} 


mysqli_close($conn);
?>
