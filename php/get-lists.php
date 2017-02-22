<?php
	$data[] = Array();
	session_start();

	$user = $_SESSION["DisplayName"];

	# Connect to database
	$db = new mysqli('localhost', 'root', '', 'CommunityRate');
	if ($db->connect_error):
		die ("Could not connect to db: " . $db->connect_error);
	endif;

	# 1. Find the lists belonging to this user
	$find_lists = "SELECT * FROM Lists where Lists.Creator = '$user'";
	$result = $db->query($find_lists);
	$rows = $result->num_rows;
	for($i = 0; $i < $rows; $i++) {
		$row = $result->fetch_array();
		$data[] = $row;
	}
	
	$response = json_encode($data);
	echo "$response";
?>