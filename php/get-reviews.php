<?php
	session_start();
	$userID = $_SESSION["user"][0];

	$db = new mysqli('localhost','root','','CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db " . $db->connect_error);
		endif;

	$result = $db->query("SELECT * FROM Reviews WHERE User_ID = $userID");
	if ($result->num_rows > 0) {
		for ($i = 0; $i < $result->num_rows; $i++) {
			$review = $result->fetch_array();
			$reviews[] = $review;
		}
		echo json_encode($reviews);
	}
	else {
		echo "none";
	}
?>	