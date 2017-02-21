<?php
	$db = new mysqli('localhost','root','','CommunityRate');
	if ($db->connect_error):
		die ("Could not connect to db " . $db->connect_error);
	endif;

	#drop tables
	$db->query("DROP TABLE Users");
	$db->query("DROP TABLE Reviews");
	$db->query("DROP TABLE Friendships");

	#create tables
	$db->query("CREATE TABLE Users (ID bigint primary key NOT NULL AUTO_INCREMENT, fb_ID bigint, Name char(50), Email char(35), DisplayName char(35), Password char(35))") or die ("Invalid create " . $db->error);
	$db->query("CREATE TABLE Reviews (Movie_ID bigint(20), User_ID int(20), Rating float, Thoughts text, DateReviewed datetime DEFAULT CURRENT_TIMESTAMP)") or die ("Invalid create " . $db->error);
	$db->query("CREATE TABLE Friendships (Follower bigint(20), Followee bigint(20), DateAdded datetime DEFAULT CURRENT_TIMESTAMP)");
	echo "Setup Users, Reviews, Friendships tables in CommunityRate DB"
?>