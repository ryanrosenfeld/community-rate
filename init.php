<?php
	$db = new mysqli('localhost','root','','CommunityRate');
	if ($db->connect_error):
		die ("Could not connect to db " . $db->connect_error);
	endif;

	#drop tables
	$db->query("DROP TABLE Movies");
	$db->query("DROP TABLE Users");
	$db->query("DROP TABLE Reviews");

	#create tables
	$db->query("CREATE TABLE Movies (ID int primary key AUTO_INCREMENT, Title char(35), Rating float default 0.0)") or die ("Invalid create " . $db->error);
	$db->query("CREATE TABLE Users (ID int primary key NOT NULL AUTO_INCREMENT, LastName char(35) NOT NULL, FirstName char(35), Email char(35), DisplayName char(35), Password char(35))");
	$db->query("CREATE TABLE Reviews (Movie_ID int, User_ID int, Rating float, Thoughts text)");

	#add sample user
	$query = "INSERT INTO Users (LastName, FirstName, Email, DisplayName, Password) VALUES('Rosenfeld', 'Ryan', 'rdr6re@virginia.edu', 'Ryan', 'test')";
	$db->query($query);

	#add movies into DB
	$movies = file("movies.txt");
	foreach($movies as $m) {
		$m = addslashes(rtrim($m));
		$query = "INSERT INTO Movies (Title) values ('$m')";
		$db->query($query) or die ("Invalid insert " . $db->error);
	}
?>