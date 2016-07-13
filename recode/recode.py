import os,time,sys,pymysql,shutil

def recode(a):
	global folder,dest
	shutil.copy(folder+a.replace('.avi','P.jpg'),dest+a.replace('.avi','.jpg'))
	os.chdir(dest)
	cmd="ffmpeg -i "+ folder+a+" -vcodec h264 -an -vb 2000k -y "+a.replace('avi','mp4')
	print cmd
	return os.system(cmd)

def sqllog(a):
	global date
	conn=pymysql.connect(host='127.0.0.1',port=3306,user='meteor',passwd='bnuastro',db='meteorchaser')
	cur=conn.cursor()
	cur.execute("INSERT INTO rawdata (date,name,type) VALUES(\'"+date+"\',\'"+a[:-4]+"\',0)")
	conn.commit()
	cur.close()
	conn.close()

def main():
	global folder
	allfile=os.listdir(folder)
	for a in allfile:
		if a[-4:] == '.avi' and a[0]=='M':
			if recode(a)==0:
				sqllog(a)

if __name__ == '__main__':
	global date,folder,dest
	if len(sys.argv)>1:
		date=sys.argv[1]
	else:
		date=time.strftime('%Y%m%d')
	folder='/var/www/html/file/meteor/'+date[0:4]+'/'+date[0:6]+'/'+date[0:8]+'/'
	dest='/var/www/html/file/meteor/recoded/'+date[0:8]+'/'
	#print folder
	if not os.path.exists(dest):
		os.mkdir(dest)
	main()
