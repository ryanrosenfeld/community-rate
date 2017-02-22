<?php
	$data[] = Array();

	if(isset($_POST["list_ID"])) {
		# Connect to database
		$db = new mysqli('localhost', 'root', '', 'CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db: " . $db->connect_error);
		endif;
		$list = $_POST["list_ID"];

		# 1. Find the movie IDs belonging to this list
		$find_movies = "SELECT * FROM MovieListLines where MovieListLines.List_ID = '$list'";
		$result = $db->query($find_movies);
		$rows = $result->num_rows;
		for($i = 0; $i < $rows; $i++) {
			# 2. Get the data for each movie
			$row = $result->fetch_array();
			$movie_ID = $row["Movie_ID"];
			$find_movie = "SELECT * FROM Movies where Movies.Movie_ID = '$movie_ID'";
			$result_movie = $db->query($find_movie);
			$movie_row = $result_movie->fetch_array();
			$data[] = $movie_row;
		}
	}
	
	$response = json_encode($data);
	echo "$response";
?>