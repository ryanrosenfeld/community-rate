<?php
	header('Content-type: text/xml');
	echo "<?xml version='1.0' encoding='utf-8'?>";
	echo "<Reply>";
	if(($_POST["first"]) != '' && ($_POST["last"]) != '' && $_POST["email"] != '' && $_POST["password"] != '' && $_POST["display"] != '') {
		$name = $_POST["first"] . " " . $_POST["last"];
		$email = $_POST["email"];
		$pw = password_hash($_POST["password"], PASSWORD_DEFAULT);
		$display = $_POST["display"];
		echo "<grr>$name</grr>";

		# Connect to database
		$db = new mysqli('localhost', 'root', '', 'CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db: " . $db->connect_error);
		endif;

		# check if user's email is already in database or display name taken
		$email_check = "SELECT * from Users where Users.Email = '$email'";
		$result =  $db->query($email_check);
		$rows_email = $result->num_rows;
		$display_check = "SELECT * from Users where Users.DisplayName = '$display'";
		$result =  $db->query($display_check);
		$rows_display = $result->num_rows;
		if($rows_email >= 1) {
			echo "<value>0</value>";
			echo "<response>$email already exists in database. </response>";
		}
		else if($rows_display >= 1) {
			echo "<value>0</value>";
			echo "<response>That username [$display] is already taken.</response>";
		}
		else {
			# insert user into table
			$sql = "INSERT INTO Users (Name, Email, DisplayName, Password) VALUES ('$name', '$email', '$display', '$pw')";
			if ($db->query($sql) === TRUE) {
				echo "<value>1</value>";
	    		echo "<response>Welcome, $name! New user [$display] added successfully.</response>";
	    		// header("Location: ../Login.html"); /* Redirect browser to the ticket page */
			} else {
	    		echo "<response>Error: " . $sql . "<br>" . $db->error . "</response>";
			}
		}
	}
	else {
		echo "<value>-1</value>";
		echo "<response>All fields are required.</response>";
	}
	echo "</Reply>";
?>