<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
=
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #d5fdd5;
}

tr:nth-child(odd) {
  background-color: #eafeea;
}

.dot {
  height: 20px;
  width: 20px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
}
</style>
<body>

<?php
require 'config.php';
date_default_timezone_set('Europe/London');

$dbh = new PDO('mysql:host=localhost;dbname=f2b', SQL_USER, SQL_PASS);

$ip = $_POST["name"];
$sql = "SELECT   hostname, created,jail, protocol, port,ip,bantime from f2b order by created";

$stmt = $dbh->prepare($sql);
//$stmt->bindParam(':ip', $ip, PDO::PARAM_STR);
$stmt->execute();

#echo 'created  jail protocol port ip bantime <br>';

echo '<table id="myTable" class="display"   cellspacing="0" width="100%">' . "\n";

$header =
    '<tr>' . "\n" .
    ' <th></th>' . "\n" .
    ' <th>created</th>' . "\n" .
    ' <th>jail</th>' . "\n" .
    ' <th>protocol</th>' . "\n" .
    ' <th>port</th>' . "\n" .
    ' <th>ip</th>' . "\n" .
    ' <th>bantime</th>' . "\n" .
    ' <th></th>' . "\n" .
    '</tr>' . "\n";

echo $header;
if ($stmt->rowCount() > 0) {

    foreach ($stmt->fetchAll(PDO::FETCH_ASSOC) as $row) {

        $created = $row['created'];
        $jail = $row['jail'];
        $protocol = $row['protocol'];
        $port = $row['port'];
        $ip = $row['ip'];
        $bantime = $row['bantime'];

        $line = '<tr>' . "\n" .
            ' <td>   <span class="dot"></span>   </td>' . "\n" .
            ' <td>' . $created . '</td>' . "\n" .
            ' <td>' . $jail . '</td>' . "\n" .
            ' <td>' . $protocol . '</td>' . "\n" .
            ' <td>' . $port . '</td>' . "\n" .
            ' <td>' . $ip . '</td>' . "\n" .
            ' <td>' . $bantime . '</td>' . "\n" .
            ' <td>   <span class="dot"></span>   </td>' . "\n" .
            '</tr>' . "\n";
        echo $line;

    }
}

echo '</table>' . "\n";
?>

</body>
</html>
