<?php
	session_start();

	$db = new mysqli('localhost','root','','CommunityRate');
	if ($db->connect_error):
		die ("Could not connect to db " . $db->connect_error);
	endif;

	$id = $_SESSION["user"][0];

	#Get Followers
	$result = $db->query("SELECT * FROM Friendships JOIN Users ON Friendships.Follower = Users.ID WHERE Followee = $id");
	$followers = array();
	for ($i = 0; $i < $result->num_rows; $i++) {
		$followers[] = $result->fetch_array();
	}
	$friendships[] = $followers;

	#Get Followees
	$result = $db->query("SELECT * FROM Friendships JOIN Users ON Friendships.Followee = Users.ID WHERE Follower = $id");
	$followees = array();
	for ($i = 0; $i < $result->num_rows; $i++) {
		$followees[] = $result->fetch_array();
	}
	$friendships[] = $followees;

	echo json_encode($friendships);