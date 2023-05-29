<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $jsonPayload = file_get_contents('php://input');

  echo "Data JSON yang diterima: ";
  echo $jsonPayload;
}
?>
