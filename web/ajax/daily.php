<?php

//ini_set("display_errors", "On");
//error_reporting(E_ALL | E_STRICT);


header("charset=utf-8");
if ($_GET["date"]!=""){
	
	if(!$GLOBALS['db']=mysql_connect('127.0.0.1','meteor','bnuastro')) 
		echo 'why?';
	if(!mysql_select_db('meteorchaser')) 
		echo 'why?2';
	$date=mysql_real_escape_string($_GET["date"]);
	$query=sprintf('SELECT name,type FROM rawdata WHERE date="%s"',$date);
	$result = mysql_query($query,$GLOBALS['db']);
	$c=0;
	$videourl=array();
	$picurl=array();
	$type=array();
	$name=array();
	while($row=mysql_fetch_array($result)){
		$c+=1;
		$v='http://meteor.bnuastro.club/file/meteor/recoded/'.$date.'/'.$row["name"].'.mp4';
		array_push($videourl,$v);
		$p='http://meteor.bnuastro.club/file/meteor/recoded/'.$date.'/'.$row["name"].'.jpg';
		array_push($picurl,$p);
		array_push($type,$row["type"]);
		array_push($name,$row["name"]);
	}
	$final["count"]=$c;
	$final["name"]=$name;
	$final["type"]=$type;
	$final["vidurl"]=$videourl;
	$final["picurl"]=$picurl;
	echo json_encode($final,JSON_UNESCAPED_SLASHES);
}
?>