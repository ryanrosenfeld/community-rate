<?php
	$db = new mysqli('localhost','root','','CommunityRate');
	if ($db->connect_error):
		die ("Could not connect to db " . $db->connect_error);
	endif;

	$result = $db->query("SELECT * FROM Users");
	$users = array();
	for ($i = 0; $i < $result->num_rows; $i++) {
		$users[] = $result->fetch_array();
	}
	echo json_encode($users);
?>