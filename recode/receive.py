# receive file from client and store them into file use asyncore.# 
#/usr/bin/python 
#coding: utf-8 
import asyncore 
import socket 
from socket import errno 
import logging 
import time 
import sys 
import struct 
import os 
import fcntl 
import threading 
from rrd_graph import MakeGraph 
try: 
  import rrdtool 
except (ImportError, ImportWarnning): 
  print "Hope this information can help you:" 
  print "Can not find pyinotify module in sys path, just run [apt-get install python-rrdtool] in ubuntu." 
  sys.exit(1) 
class RequestHandler(asyncore.dispatcher): 
  def __init__(self, sock, map=None, chunk_size=1024): 
    self.logger = logging.getLogger('%s-%s' % (self.__class__.__name__, str(sock.getsockname()))) 
    self.chunk_size = chunk_size 
    asyncore.dispatcher.__init__(self,sock,map) 
    self.data_to_write = list() 
  def readable(self): 
    #self.logger.debug("readable() called.") 
    return True 
  def writable(self): 
    response = (not self.connected) or len(self.data_to_write) 
    #self.logger.debug('writable() -> %s data length -> %s' % (response, len(self.data_to_write))) 
    return response 
  def handle_write(self): 
    data = self.data_to_write.pop() 
    #self.logger.debug("handle_write()->%s size: %s",data.rstrip('\r\n'),len(data)) 
    sent = self.send(data[:self.chunk_size]) 
    if sent < len(data): 
      remaining = data[sent:] 
      self.data_to_write.append(remaining) 
  def handle_read(self): 
    self.writen_size = 0 
    nagios_perfdata = '../perfdata' 
    head_packet_format = "!LL128s128sL" 
    head_packet_size = struct.calcsize(head_packet_format) 
    data = self.recv(head_packet_size) 
    if not data: 
      return 
    filepath_len, filename_len, filepath,filename, filesize = struct.unpack(head_packet_format,data) 
    filepath = os.path.join(nagios_perfdata, filepath[:filepath_len]) 
    filename = filename[:filename_len] 
    self.logger.debug("update file: %s" % filepath + '/' + filename)
    try: 
      if not os.path.exists(filepath): 
        os.makedirs(filepath) 
    except OSError: 
      pass 
    self.fd = open(os.path.join(filepath,filename), 'w') 
    #self.fd = open(filename,'w') 
    if filesize > self.chunk_size: 
      times = filesize / self.chunk_size 
      first_part_size = times * self.chunk_size 
      second_part_size = filesize % self.chunk_size 
      while 1: 
        try: 
          data = self.recv(self.chunk_size) 
          #self.logger.debug("handle_read()->%s size.",len(data)) 
        except socket.error,e: 
          if e.args[0] == errno.EWOULDBLOCK: 
            print "EWOULDBLOCK" 
            time.sleep(1) 
          else: 
            #self.logger.debug("Error happend while receive data: %s" % e) 
            break 
        else: 
          self.fd.write(data) 
          self.fd.flush() 
          self.writen_size += len(data) 
          if self.writen_size == first_part_size: 
            break 
      #receive the packet at last 
      while 1: 
        try: 
          data = self.recv(second_part_size) 
          #self.logger.debug("handle_read()->%s size.",len(data)) 
        except socket.error,e: 
          if e.args[0] == errno.EWOULDBLOCK: 
            print "EWOULDBLOCK" 
            time.sleep(1) 
          else: 
            #self.logger.debug("Error happend while receive data: %s" % e) 
            break 
        else: 
          self.fd.write(data) 
          self.fd.flush() 
          self.writen_size += len(data) 
          if len(data) == second_part_size: 
            break 
    elif filesize <= self.chunk_size: 
      while 1: 
        try: 
          data = self.recv(filesize) 
          #self.logger.debug("handle_read()->%s size.",len(data)) 
        except socket.error,e: 
          if e.args[0] == errno.EWOULDBLOCK: 
            print "EWOULDBLOCK" 
            time.sleep(1) 
          else: 
            #self.logger.debug("Error happend while receive data: %s" % e) 
            break 
        else: 
          self.fd.write(data) 
          self.fd.flush() 
          self.writen_size += len(data) 
          if len(data) == filesize: 
            break 
    self.logger.debug("File size: %s" % self.writen_size) 
class SyncServer(asyncore.dispatcher): 
  def __init__(self,host,port): 
    asyncore.dispatcher.__init__(self) 
    self.debug = True 
    self.logger = logging.getLogger(self.__class__.__name__) 
    self.create_socket(socket.AF_INET,socket.SOCK_STREAM) 
    self.set_reuse_addr() 
    self.bind((host,port)) 
    self.listen(2000) 
  def handle_accept(self): 
    client_socket = self.accept() 
    if client_socket is None: 
      pass 
    else: 
      sock, addr = client_socket 
      #self.logger.debug("Incoming connection from %s" % repr(addr)) 
      handler = RequestHandler(sock=sock) 
class RunServer(threading.Thread): 
  def __init__(self): 
    super(RunServer,self).__init__() 
    self.daemon = False 
  def run(self): 
    server = SyncServer('',9999) 
    asyncore.loop(use_poll=True) 
def StartServer(): 
  logging.basicConfig(level=logging.DEBUG, 
            format='%(name)s: %(message)s', 
            ) 
  RunServer().start() 
  #MakeGraph().start() 
if __name__ == '__main__': 
  StartServer()
