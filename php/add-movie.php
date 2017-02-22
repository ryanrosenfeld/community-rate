<?php
	session_start();

	$db = new mysqli('localhost','root','','CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db " . $db->connect_error);
		endif;

	if (isset($_POST["name"]) && isset($_POST["list_ID"])) {
		$name = $_POST["name"];
		$list_ID = $_POST["list_ID"];
		$result = $db->query("SELECT * FROM Movies WHERE Movies.Name = '$name'");

		if($result->num_rows == 0) {
			$db->query("INSERT INTO Movies (Name, AvgReview, ImageName) VALUES ('$name', '-1', 'default.jpg')") or die ("Invalid Movies insert: " . $db->error);
			$result = $db->query("SELECT * FROM Movies WHERE Movies.Name = '$name'") or die ("Invalid Movies select: " . $db->error);
			$movie_ID = $result->fetch_array()["Movie_ID"];
			echo "success -- new movie added\n";

		}
		else {
			$movie_ID = $result->fetch_array()["Movie_ID"];
			echo "success -- old movie added\n";
		}
		
		$db->query("INSERT INTO MovieListLines (Movie_ID, List_ID) VALUES ('$movie_ID', '$list_ID')") or die ("Invalid MovieListLines insert: " . $db->error);
		echo "added new connection";



	}
?>