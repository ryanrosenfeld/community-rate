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

	if(isset($_POST["email"]) && isset($_POST["password"])) {

		$email = $_POST["email"];
		$password = $_POST["password"];

		$db = new mysqli('localhost', 'root', '', 'CommunityRate');
			if ($db->connect_error):
				die ("Could not connect to db: " . $db->connect_error);
			endif;

		# check if user in database
		$sql = "SELECT * from Users where Users.Email = '$email'";
		$result =  $db->query($sql);
		$rows = $result->num_rows;

		# Email address not found in DB - alert user
		if($rows == 0) {
			$message = "Email address not found.";
			echo "<SCRIPT type='text/javascript'> alert('$message'); 
				window.location = \"../login.html\"; </SCRIPT>";
		}

		$row = $result->fetch_array();

		#check password
		if(password_verify($password, $row["Password"])) {
			$_SESSION["user"] = $row;
			$_SESSION["DisplayName"] = $row["DisplayName"];
			header("Location: ../profile.html");
		}
		else {
			# Incorrect password - alert user
			$message = "Incorrect email address and password combination";
			echo "<SCRIPT type='text/javascript'> alert('$message');
        		window.location = \"../login.html\"; </SCRIPT>";
		}
	}
?>