<?php
//ini_set("display_errors", "Off");
date_default_timezone_set('prc');

$t1 = microtime(true);

$con=mysqli_connect("localhost","meteor","bnuastro","meteorchaser");  
if (mysqli_connect_errno($con)){  
    echo "连接 MySQL 失败: " . mysqli_connect_error();  
}  

$query="SELECT substring(name,2,11) FROM webmeteor";
$result=mysqli_query($con,$query); 
$rows=mysqli_fetch_all($result,MYSQLI_ASSOC); 
mysqli_free_result($result); 
$rerow=array_column($rows,'substring(name,2,11)');
$detect=array_count_values($rerow);

$query="SELECT substring(name,2,11) FROM webmeteor WHERE type=1";
$result=mysqli_query($con,$query); 
$rows=mysqli_fetch_all($result,MYSQLI_ASSOC); 
mysqli_free_result($result); 
$rerow=array_column($rows,'substring(name,2,11)');
$meteorconfirm=array_count_values($rerow);
//print_r($meteorcount);

$query="SELECT hour,cloudrate,pm25 FROM weather";
$result=mysqli_query($con,$query); 
$rows=mysqli_fetch_all($result,MYSQLI_ASSOC);
$cloudrate= array_column($rows,'cloudrate','hour');
$pm25= array_column($rows,'pm25','hour');

mysqli_close($con); 

//print_r($pm25);
$ny=intval(date("Y"));
$nm=intval(date("m"));
$nd=intval(date("d"));
$nH=intval(date("H"));
$d=mktime(0,0,0,8,10,2016);
$n=time();
$temmeteor=array();
$temcloudrate=array();
$tempm25=array();
while($d<$n){
	$times[]=date("Y/n/j G:i", $d);
	if (array_key_exists(date("Ymd_H",$d),$detect)){
		$temdetect[]=$detect[date("Ymd_H",$d)];
	}
	else{
		$temdetect[]=0;
	}
	if (array_key_exists(date("Ymd_H",$d),$meteorconfirm)){
		$temmeteor[]=$meteorconfirm[date("Ymd_H",$d)];
	}
	else{
		$temmeteor[]=0;
	}
	if (array_key_exists(date("YmdH",$d),$cloudrate)){
		$temcloudrate[]=floatval($cloudrate[date("YmdH",$d)]);
	}
	else{
		$temcloudrate[]=0;
	}
	if (array_key_exists(date("YmdH",$d),$pm25)){
		$tempm25[]=floatval($pm25[date("YmdH",$d)]);
	}
	else{
		$tempm25[]=0;
	}
	$nothing[]=0.5;
	$d=strtotime("+1 Hour",$d);
}
$final['time']=$times;
$final['detect']=$temdetect;
$final['meteor']=$temmeteor;
$final['cloudrate']=$temcloudrate;
$final['pm25']=$tempm25;

$d=mktime(0,0,0,8,10,2016);
$n=time();
$temperiod=array();
$c=0;
while($d<$n){
	$csvpath=sprintf('D:\\meteor\\%s\\%s\\detlog.csv',date('Y',$d),date('Ym',$d));
	$myfile = fopen($csvpath, "r");
	fgets($myfile);
	while(!feof($myfile)) {
		$str=explode(',',fgets($myfile));
		if($str[1]!='' && count($str)>8){
			$temperiod[]=array();
			$onep=mktime(intval($str[4]),0,0,intval($str[2]),intval($str[3]),intval($str[1]));
			$temperiod[$c][0]=date("Y/n/j G:00", $onep);
			$onep=mktime(intval($str[10]),0,0,intval($str[8]),intval($str[9]),intval($str[7]));
			$temperiod[$c][1]=date("Y/n/j G:00", $onep);
			$c+=1;
		}
	}
	if($str[1]!='' && count($str)<9){
		$onep=mktime(intval($str[4]),0,0,intval($str[2]),intval($str[3]),intval($str[1]));
		if(time()-$onep<43200){
			$temperiod[]=array();
			$temperiod[$c][0]=date("Y/n/j G:00", $onep);
			$temperiod[$c][1]=date("Y/n/j G:00", time());
		}
	}
	$d=strtotime("+1 Month",$d);
}
$final['period']=$temperiod;

$t2 = microtime(true);
$final['php']=round($t2-$t1,3);

echo json_encode($final,JSON_UNESCAPED_SLASHES);
?>
