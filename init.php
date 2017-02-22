<?php
	$db = new mysqli('localhost','root','','CommunityRate');
	if ($db->connect_error):
		die ("Could not connect to db " . $db->connect_error);
	endif;

	#drop tables
	$db->query("DROP TABLE Users");
	$db->query("DROP TABLE Reviews");
	$db->query("DROP TABLE Friendships");
	$db->query("DROP TABLE Lists");
	$db->query("DROP TABLE Movies");
	$db->query("DROP TABLE MovieListLines"); // maps one movie to one list

	#create tables
	$db->query("CREATE TABLE Users (ID bigint primary key NOT NULL AUTO_INCREMENT, fb_ID bigint, Name char(50), Email char(50), DisplayName char(35), Password char(100))") or die ("Invalid create Users " . $db->error);
	
	$db->query("CREATE TABLE Reviews (Movie_ID bigint(20), User_ID int(20), Rating float, Thoughts text, DateReviewed datetime DEFAULT CURRENT_TIMESTAMP)") or die ("Invalid create Reviews " . $db->error);
	
	$db->query("CREATE TABLE Friendships (Follower bigint(20), Followee bigint(20), DateAdded datetime DEFAULT CURRENT_TIMESTAMP)") or die ("Invalid create Friendships " . $db->error);

	// creator = display name of person who created the list
	$db->query("CREATE TABLE Lists (ID bigint primary key NOT NULL AUTO_INCREMENT, Name char(50), Creator char(35), Description char(140))") or die ("Invalid create Lists " . $db->error);

	$db->query("CREATE TABLE Movies (Movie_ID bigint(20) primary key NOT NULL AUTO_INCREMENT, Name char(50), AvgReview float, ImageName char(50))") or die ("Invalid create Movies " . $db->error);

	$db->query("CREATE TABLE MovieListLines (Movie_ID bigint(20) NOT NULL, List_ID bigint NOT NULL)") or die ("Invalid create MovieListLines " . $db->error);

	# Success!
	echo "Setup 6 tables in CommunityRate DB";
?>