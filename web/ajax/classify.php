<?php
//echo $_GET["name"].','.$_GET["type"];
ini_set("display_errors", "Off");
header("charset=utf-8");
require 'sqlcon.php';
if ($_GET["name"]!="" && $_GET["type"]!=""){
	$name=mysql_real_escape_string($_GET["name"]);
	$type=mysql_real_escape_string($_GET["type"]);
	$query=sprintf('UPDATE webmeteor SET type=%s WHERE name="%s"',$type,$name);
	mysql_query($query,$GLOBALS['db']);
	echo 'Done';
}
?>