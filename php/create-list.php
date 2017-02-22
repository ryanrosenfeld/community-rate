<?php
	header('Content-type: text/xml');
	echo "<?xml version='1.0' encoding='utf-8'?>";
	echo "<Reply>";
	if(isset($_POST["name"]) && isset($_POST["description"])) {
		session_start();
		$list_name = $_POST["name"];
		$user = $_SESSION["DisplayName"];
		$description = $_POST["description"];

		# Connect to database
		$db = new mysqli('localhost', 'root', '', 'CommunityRate');
		if ($db->connect_error):
			die ("Could not connect to db: " . $db->connect_error);
		endif;

		# check if list name is already in database
		$check = "SELECT * from Lists where Lists.Name = '$list_name'";
		$result =  $db->query($check);
		$rows = $result->num_rows;
		if($rows >= 1) {
			echo "<response>$list_name already exists in database. </response>";
		}
		else {
			# insert list into table
			$sql_lists = "INSERT INTO Lists (Name, Creator, Description) VALUES ('$list_name', '$user', '$description')";
			if ($db->query($sql_lists)) {
				// $select1 = "SELECT * FROM Lists WHERE Lists.Name = '$list_name'";
				// $result = $db->query($select1);
				// $row = $result->fetch_array();
				// $list_ID = $row["ID"];

				// $list_lines = "INSERT INTO UserListLines (List_ID, User_DisplayName) VALUES ('$list_ID', '$user')";
				// // TODO : move them to new list page
	   //  		// header("Location: ../Login.html"); /* Redirect browser to the ticket page */
	   //  		if($db->query($list_lines)) {
					echo "<response>Successfully added [$list_name] to database. </response>";
//	    		}
	    		// else {
	    		// 	echo "<response>Error during UserListLines insertion: " . $db->error . "</response>";
	    		// }
			} else {
	    		echo "<response>Error during Lists insertion: " . $db->error . "</response>";
			}
		}
	}
	else {
		echo "<response>All fields are required.</response>";
	}
	echo "</Reply>";
?>