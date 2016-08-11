<?php
ini_set("display_errors", "Off");
date_default_timezone_set('prc');
require 'sqlcon.php';
$filesnames = scandir('D:\\meteor\\recoded\\'.date('Ymd',time()));
$c=0;
foreach ($filesnames as $name) {
	if(substr($name,-4)=='.mp4'){
		$c+=1;
	}
}
$query=sprintf('SELECT temperature,humidity,pm25,skycon,cloudrate FROM weather WHERE hour="%s"',date('YmdH',time()));
$result = mysql_query($query,$GLOBALS['db']);
$row=mysql_fetch_array($result,MYSQL_ASSOC);
$row['count']=$c;
echo json_encode($row,JSON_UNESCAPED_SLASHES);
?>