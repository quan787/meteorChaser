import win32file,pymysql
from VideoCapture import Device
import time,math,urllib,json,os

# Get the all files & directories in the specified directory (path).
def get_recursive_file_list(path):
    current_files = os.listdir(path)
    all_files = []
    for file_name in current_files:
        full_file_name = os.path.join(path, file_name)
        if file_name[-4:]=='.avi' and file_name[0]=='M':
            all_files.append(full_file_name)
        if file_name[-4:]=='.csv':
            win32file.CopyFileW(full_file_name,full_file_name.replace('C','D'),0)
        if os.path.isdir(full_file_name):
            next_level_files = get_recursive_file_list(full_file_name)
            all_files.extend(next_level_files)
    return all_files
def move_recode():
    allavi=get_recursive_file_list("C:\\meteor\\2016")
    for fullname in allavi:
        copyname=fullname.replace('C','D')
        if not os.path.exists(copyname[0:30]):
            os.mkdirs(copyname[0:30])
        win32file.CopyFileW(fullname,copyname,0)
        destfile='D:\\meteor\\recoded\\'+fullname[22:-4]+'.mp4'
        if not os.path.exists(destfile[0:26]):
            os.mkdir(destfile[0:26])
        cmd="ffmpeg -i "+ fullname+" -vcodec h264 -an -vb 2000k -y "+destfile
        if os.system(cmd)==0:
            print destfile,'Done.'
            win32file.DeleteFile(fullname)
        win32file.CopyFileW(fullname[0:-4]+'.xml',copyname[0:-4]+'.xml',0)
        win32file.CopyFileW(fullname[0:-4]+'M.bmp',copyname[0:-4]+'M.bmp',0)
        win32file.CopyFileW(fullname[0:-4]+'P.bmp',copyname[0:-4]+'P.bmp',0)
        win32file.CopyFileW(fullname[0:-4]+'P.jpg',copyname[0:-4]+'P.jpg',0)
        win32file.CopyFileW(fullname[0:-4]+'P.jpg','D:\\meteor\\realtime.jpg',0)
        win32file.CopyFileW(fullname[0:-4]+'P.jpg',destfile[0:-4]+'.jpg',0)
        win32file.CopyFileW(fullname[0:-4]+'T.jpg',copyname[0:-4]+'T.jpg',0)
        win32file.DeleteFile(fullname[0:-4]+'.xml')
        win32file.DeleteFile(fullname[0:-4]+'M.bmp')
        win32file.DeleteFile(fullname[0:-4]+'P.bmp')
        win32file.DeleteFile(fullname[0:-4]+'P.jpg')
        win32file.DeleteFile(fullname[0:-4]+'T.jpg')
        sqllog(fullname[22:30],fullname[31:-4])
def calsr(days,lat,lon,timezone):
    sr=24*(180+timezone*15-lon-math.degrees(math.acos(-math.tan(math.radians(-23.4*math.cos(360*(days+9)/365)))*math.tan(math.radians(lat)))))/360
    ss=24*(1+(timezone*15-lon)/180)-sr
    return (sr,ss)
def sqllog(date,name):
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='meteor',passwd='bnuastro',db='meteorchaser')
    cur=conn.cursor()
    cur.execute("INSERT INTO webmeteor (date,name,type) VALUES(\'"+date+"\',\'"+name+"\',0)")
    conn.commit()
    cur.close()
    conn.close()

def logweather():
    f=urllib.urlopen("https://api.caiyunapp.com/v2/cAP9tPF0hIcuTofj/116.3608,39.9586/realtime.json")
    s=f.read()
    arr=json.loads(s)
    hour=time.strftime("%Y%m%d%H")
    temperature=str(arr['result']["temperature"])
    skycon=arr['result']["skycon"]
    cloudrate=str(arr['result']["cloudrate"])
    aqi=str(arr['result']["aqi"])
    humidity=str(arr['result']["humidity"])
    pm25=str(arr['result']["pm25"])
    intensity=str(arr['result']["precipitation"]["local"]["intensity"])
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='meteor',passwd='bnuastro',db='meteorchaser')
    cur=conn.cursor()
    cur.execute("INSERT INTO weather (hour,temperature,skycon,cloudrate,aqi,humidity,pm25,intensity) VALUES(\'"+hour+"\',"+temperature+",\'"+skycon+"\',"+cloudrate+","+aqi+","+humidity+","+pm25+","+intensity+"0)")
    conn.commit()
    cur.close()
    conn.close()

def main():
    print "Please Keep Running This Thing"
    lat=40.0
    lon=116.4
    timezone=8
    hour=11
    while True:
        if hour!=int(time.strftime("%H")):
            if hour==11:
                days=int(time.strftime('%j'))
                (sr,ss)=calsr(days,lat,lon,timezone)
            hour=int(time.strftime("%H"))
            logweather()
        if int(time.strftime("%H"))+1.0/60*int(time.strftime("%M"))>=ss+0.5 or int(time.strftime("%H"))+1.0/60*int(time.strftime("%M"))<=sr-0.5:
            move_recode()
        else:
            cam=Device()
            cam.saveSnapshot("D:/meteor/realtime.jpg",timestamp=3,textpos='bl')
            del cam
        time.sleep(120)
if __name__ == '__main__':
    main()
