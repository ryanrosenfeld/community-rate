<?php
	session_start();
	if (isset($_SESSION["user"])) {
		$userID = $_SESSION["user"][0];
	}

	$db = new mysqli('localhost','root','','CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db " . $db->connect_error);
		endif;

	$result = $db->query("SELECT * FROM Reviews WHERE User_ID = $userID");
	for ($i = 0; $i < $result->num_rows; $i++) {
		$review = $result->fetch_array();
		$reviews[] = $review;
	}
	
	for ($i = 0; $i < sizeof($reviews); $i++) {
		$movieID = $reviews[$i][0];
		$movie = $db->query("SELECT Title FROM Movies WHERE ID = $movieID");
		$movie = $movie->fetch_array();
		$movieNames[$movie[0]] = $reviews[$i][2];
	}

	echo json_encode($reviews);
	echo "#";
	echo json_encode($movieNames);
?>