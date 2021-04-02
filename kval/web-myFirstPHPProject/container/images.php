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


if (isset($_GET["filename"])){
	//$fn = __DIR__."/".$upload_dir.(basename($_GET['filename']));
	$fn = $upload_dir.(basename($_GET['filename']));
	$img = base64_encode(file_get_contents($fn));
	echo "<img width=200px height=200px src='data:image;base64, ".$img."' />";
}

?>

<h1>Image Uploader</h1>
Upload an image and share the obtained URL with your friends. How fun!

<form action="images.php" method="post" enctype="multipart/form-data">
  Select an image to upload:
  <input type="file" name="fileToUpload" id="fileToUpload"><br />
  <input type="submit" value="Upload Image" name="submit">
</form>

<?php
if (isset($_FILES["fileToUpload"])){
	echo "<p class='error' >";
	$file_name = md5_file($_FILES["fileToUpload"]["tmp_name"]).$_FILES["fileToUpload"]["name"];
	echo ($file_name);
	$target_file = __DIR__."/".$upload_dir . basename($file_name);
	$uploadOk = 1;
	$file = $_FILES["fileToUpload"]["name"];

	// Check the file extension
	$extension = explode(".", $file)[1];
	if ($extension == "jpeg" || $extension == "jpg" || $extension == "png") {
	    $uploadOk = 1;
	} else {
	    //Of course the user should know what went wrong!
	    echo "Only JPG/JPEG and PNG files are allowed<br/>";
	    $uploadOk = 0;
	}

	// Check file size
	if ($_FILES["fileToUpload"]["size"] > 150000) {
	  echo "Sorry, your file is too large.<br/>";
	  $uploadOk = 0;
	}

	if ($uploadOk == 0) {
	  echo "Sorry, your file was not uploaded.<br/>";
	} else {
		if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
			$URL = "/images.php?filename=".$file_name;
	    	echo "</p><p class='success'>The file ". htmlspecialchars(basename($file_name))." has been uploaded.<br/>";
	    	echo "Share it with your friends using this link: <a href=".$URL.">".$URL."</a>";
	  	} else {
	    echo "Sorry, there was an error uploading your file.<br/>";
	  }
	}
	echo "</p>";
}
?>


</body>
</html>
