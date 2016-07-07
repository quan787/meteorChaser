# monitor path with inotify(python module), and send them to remote server.# 
# use sendfile(2) instead of send function in socket, if we have python-sendfile installed.# 
import socket 
import time 
import os 
import sys 
import struct 
import threading 
import Queue 
try: 
   import pyinotify 
except (ImportError, ImportWarnning): 
   print "Hope this information can help you:" 
   print "Can not find pyinotify module in sys path, just run [apt-get install python-pyinotify] in ubuntu." 
   sys.exit(1) 
try: 
   from sendfile import sendfile 
except (ImportError,ImportWarnning): 
   pass 
filetype_filter = [".rrd",".xml"] 
def check_filetype(pathname): 
   for suffix_name in filetype_filter: 
     if pathname[-4:] == suffix_name: 
       return True 
   try: 
     end_string = pathname.rsplit('.')[-1:][0] 
     end_int = int(end_string) 
   except: 
     pass 
   else: 
     # means pathname endwith digit 
     return False 
class sync_file(threading.Thread): 
   def __init__(self, addr, events_queue): 
     super(sync_file,self).__init__() 
     self.daemon = False 
     self.queue = events_queue 
     self.addr = addr 
     self.chunk_size = 1024 
   def run(self): 
     while 1: 
       event = self.queue.get() 
       if check_filetype(event.pathname): 
         print time.asctime(),event.maskname, event.pathname 
         filepath = event.path.split('/')[-1:][0] 
         filename = event.name 
         filesize = os.stat(os.path.join(event.path, filename)).st_size 
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
         filepath_len = len(filepath) 
         filename_len = len(filename) 
         sock.connect(self.addr) 
         offset = 0 
         data = struct.pack("!LL128s128sL",filepath_len, filename_len, filepath,filename,filesize) 
         fd = open(event.pathname,'rb') 
         sock.sendall(data) 
         if "sendfile" in sys.modules: 
           # print "use sendfile(2)" 
           while 1: 
             sent = sendfile(sock.fileno(), fd.fileno(), offset, self.chunk_size) 
             if sent == 0: 
               break 
             offset += sent 
         else: 
           # print "use original send function" 
           while 1: 
             data = fd.read(self.chunk_size) 
             if not data: break 
             sock.send(data) 
         sock.close() 
         fd.close() 
class EventHandler(pyinotify.ProcessEvent): 
   def __init__(self, events_queue): 
     super(EventHandler,self).__init__() 
     self.events_queue = events_queue 
   def my_init(self): 
     pass 
   def process_IN_CLOSE_WRITE(self,event): 
     self.events_queue.put(event) 
   def process_IN_MOVED_TO(self,event): 
     self.events_queue.put(event) 
def start_notify(path, mask, sync_server): 
   events_queue = Queue.Queue() 
   sync_thread_pool = list() 
   for i in range(500): 
     sync_thread_pool.append(sync_file(sync_server, events_queue)) 
   for i in sync_thread_pool: 
     i.start() 
   wm = pyinotify.WatchManager() 
   notifier = pyinotify.Notifier(wm,EventHandler(events_queue)) 
   wdd = wm.add_watch(path,mask,rec=True) 
   notifier.loop() 
def do_notify(): 
   perfdata_path = '/var/lib/pnp4nagios/perfdata' 
   mask = pyinotify.IN_CLOSE_WRITE|pyinotify.IN_MOVED_TO 
   sync_server = ('127.0.0.1',9999) 
   start_notify(perfdata_path,mask,sync_server) 
if __name__ == '__main__': 
   do_notify()
