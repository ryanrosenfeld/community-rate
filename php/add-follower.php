<?php
	$db = new mysqli('localhost','root','','CommunityRate');
	if ($db->connect_error):
		die ("Could not connect to db " . $db->connect_error);
	endif;

	if (isset($_POST["follower"]) && isset($_POST["followee"])) {
		$follower = $_POST["follower"];
		$followee = $_POST["followee"];
		$result = $db->query("SELECT * FROM Friendships WHERE Follower = $follower & Followee = $followee");
		if ($result->num_rows === 0) {
			$db->query("INSERT INTO Friendships (Follower, Followee) VALUES ($follower, $followee)") or die ("Invalid insert " . $db->error);
			echo "success";
		}
		else {
			echo "duplicate";
		}
	}
?>