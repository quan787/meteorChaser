function GetXmlHttpObject(){
	var xmlHttp=null;
	try{
		xmlHttp=new XMLHttpRequest();
	}
	catch (e){
		try{
			xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch (e){
			xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
		}
	}
	return xmlHttp;
}
function GetStrDate(){
	var myDate = new Date();
	y=''+myDate.getFullYear();
	if(myDate.getMonth()<9) m='0'+(myDate.getMonth()+1);
	else m=''+(myDate.getMonth()+1);
	if(myDate.getDate()<10) d='0'+myDate.getDate();
	else d=''+myDate.getDate();
	return(y+m+d);
}
