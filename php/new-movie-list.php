<?php
// This is outdated -- we could probably delete it, but I'll keep it for now.
	session_start();

	$db = new mysqli('localhost','root','','CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db " . $db->connect_error);
		endif;

	if (isset($_POST["movie"]) && isset($_POST["name"])) {
		$movie = $_POST["movie"];
		$name = $_POST["name"];
		$db->query("INSERT INTO Movies VALUES ('$movie')") or die ("Invalid insert: " . $db->error);
	}

	$movies = $db->query("SELECT * FROM Movies");
	$enteredMovies = Array();
	for ($i = 0; $i < $movies->num_rows; $i++) {
		$movie = $movies->fetch_array();
		$enteredMovies[] = $movie[0];
	}
	foreach($enteredMovies as $m) {
		echo "$m#";
	}
?>