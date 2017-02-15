<?php
	session_start();

	#Initialize DB
	$db = new mysqli('localhost', 'root', '', 'CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db: " . $db->connect_error);
		endif;

	#Handle FB Login
	if (isset($_POST["fbLogin"])) {
		$name = $_POST["name"];
		$id = $_POST["id"];
		$query = "SELECT * FROM Users WHERE fb_ID = $id";
		$result = $db->query($query) or die ("Invalid select " . $db->error);
		if ($result->num_rows > 0) {
			$_SESSION["user"] = $result->fetch_array();
			echo "success";
		}
		else {
			$db->query("INSERT INTO Users (`fb_ID`, `Name`) VALUES ($id, '$name')") or die ("Invalid insert: " . $db->error);
			$result = $db->query("SELECT * FROM Users WHERE fb_ID = $id") or die ("Invalid select " . $db->error);
			$_SESSION["user"] = $result->fetch_array();
			echo "success";
		}
	}

	if (isset($_POST["email"])) {
		$email = $_POST["email"];
		$password = $_POST["password"];
		$query = "SELECT * FROM Users WHERE Email = '$email' && Password = '$password'";
		$users = $db->query($query);
		if ($users->num_rows > 0) {
			$_SESSION["user"] = $users->fetch_array();
			header("Location: ../profile.html");
		}
		else {
			echo "<p style='Color:Red'>Incorrect Username or Password</p>";
		}
	}
?>