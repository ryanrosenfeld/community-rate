<?php
	session_start();
	if (isset($_POST["email"])) {
		$email = $_POST["email"];
		$password = $_POST["password"];
		$db = new mysqli('localhost', 'root', '', 'CommunityRate');
			if ($db->connect_error):
				die ("Could not connect to db: " . $db->connect_error);
			endif;
		$query = "SELECT * FROM Users WHERE Email = '$email' && Password = '$password'";
		$users = $db->query($query);
		if ($users->num_rows > 0) {
			$_SESSION["user"] = $users->fetch_array();
			header("Location: profile.html");
		}
		else {
			echo "<p style='Color:Red'>Incorrect Username or Password</p>";
		}
	}
?>
<html>
<head>
	<title>CommunityRate</title>
</head>
<body>
	<div class="buttonDiv">
		<h3>Sign in below!</h3>
		<form action = "login.php" method = "POST">
			Email: <input type="text" name="email" size="30" maxlength="30" required><br/>
			Password: <input type="text" name="password" size="30" maxlength="30" required><br/>
			<input type="submit" class="button" value="Submit">
		</form>
		<a href="new-user.php">New User?</a>
	</div>
</body>
</html>