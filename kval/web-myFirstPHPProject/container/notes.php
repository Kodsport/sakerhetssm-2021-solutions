<!DOCTYPE html>
<html>
<head>
<title>Image Uploader</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<?php
error_reporting(0);
ini_set('display_errors', '0');
include "navigation.php";
include "constants.php";

if (isset($_POST["noteTitle"]) and isset($_POST["noteContent"])){
	$nT = preg_replace("/[^a-zA-Z0-9 ]+/", "", $_POST["noteTitle"]);
	$nC = preg_replace("/[^a-zA-Z0-9 \.,:;!?']+/", "", $_POST["noteContent"]);
	$fid = fopen($upload_dir.$nT.".txt", "w");
	fwrite($fid, $nC);
	fclose($fid);
}

?>

<h1>Notes</h1>
<p>Welcome to the notes page!</br></p>
<h2>Available Notes</h2>
<ul>

<?php
$fileList = glob($upload_dir."*");
foreach($fileList as $filename){
    if(is_file($filename)){
		$ext = pathinfo($filename, PATHINFO_EXTENSION);
		if (strtolower($ext)=="txt"){
			$filename = pathinfo($filename)['filename'];
			$URL = "/notes.php?selectedNote=".$filename.".txt";
            echo "<li><a href='".$URL."'>".$filename."</a></li>";
		}
    }
}

echo "</ul>";
if (isset($_GET["selectedNote"])){
	$nC = preg_replace("/[^a-zA-Z0-9 \.]+/", "", $_GET["selectedNote"]);
	$title = str_replace(".txt","",$nC);
	echo "<h2>Content of ".$title."</h2>";
	include $upload_dir.$nC;
}
?>
<h2>Submit a Note!</h2>
<br/>Use the form below to submit a note!</p>

<form action="notes.php" method="post" enctype="multipart/form-data">
  Title:   <input class="inputTitle" type="text" name="noteTitle" id="noteTitle"><br />
  Content: <input class="inputContent" type="text" name="noteContent" id="noteContent"><br />
  <input type="submit" value="Submit" name="submit">
</form>

</body>
</html>
