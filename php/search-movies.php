<?php
	session_start();

	$db = new mysqli('localhost','root','','CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db " . $db->connect_error);
		endif;

	if (isset($_POST["search"])) {
		$search = $_POST["search"];
		$movie = $db->query("SELECT * FROM Movies WHERE Title LIKE '%$search%'");
		if ($movie->num_rows > 0) {
			$movie = $movie->fetch_array();
			$movie = implode("#", $movie);
			echo $movie;
		}
		else {
			echo "Movie not found";
		}
	}
?>