<?php
	session_start();
	if (isset($_SESSION["user"])) {
		$userID = $_SESSION["user"][0];
	}

	$db = new mysqli('localhost','root','','CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db " . $db->connect_error);
		endif;

	if (isset($_POST["score"]) && isset($_POST["movie"])) {
		$rating = $_POST["score"];
		$thoughts = "";
		if (isset($_POST["comment"])) {
			$thoughts = $_POST["comment"];
		}
		$movieID = $_POST["movie"];
		if (checkForReview($db, $movieID, $userID)) {
			updateReview($db, $rating, $thoughts, $userID, $movieID);
		}
		else {
			insertReview($db, $rating, $thoughts, $userID, $movieID);
		}
	}

	function checkForReview($db, $movieID, $userID) {
		$query  = "SELECT * FROM Reviews WHERE (`Movie_ID` = '$movieID' & `User_ID` = $userID)";
		$result = $db->query($query);
		if ($result->num_rows > 0) {
			$result = $result->fetch_array();
			if ($result[0] == $movieID) {
				return true;
			}
			else {
				return false;
			}
		}
		else {
			return false;
		}
	}

	function updateReview($db, $rating, $thoughts, $userID, $movieID) {
		$db->query("UPDATE Reviews SET Rating = '$rating', Thoughts = '$thoughts' WHERE User_ID = $userID & Movie_ID = $movieID") or die ("Invalid update " . $db->error);
	}

	function insertReview($db, $rating, $thoughts, $user, $movie) {
		$db->query("INSERT INTO Reviews Values ($movie, $user, $rating, '$thoughts')") or die ("Invalid insert " . $db->error);
	}
?>