<?php
  $dataFile = fopen($_POST['savetocsv'] . ".csv", 'a');
  fwrite($dataFile, "\r\n");
  fwrite($dataFile, $_POST['curData']); // append data from the subject
  fclose($dataFile);
?>
