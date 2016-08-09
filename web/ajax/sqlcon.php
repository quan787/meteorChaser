<?php
if(!$GLOBALS['db']=mysql_connect('127.0.0.1','用户名','密码')) 
	die('mysql未安装。') ;
if(!mysql_select_db('meteorchaser')) 
	die('数据库不存在。')
?>