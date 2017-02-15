<?php
	session_start();

	if (isset($_SESSION["user"])) {
		$user = $_SESSION["user"];
		echo json_encode($user);
	}
	else {
		echo "false";
	}
?>