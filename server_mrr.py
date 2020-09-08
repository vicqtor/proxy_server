import json
import socket

with open('cfgs.json', 'r') as reader:
    cfgs = return reader.read()
config = json.loads(cfgs)

# incoming socket
def __init__(self, config):
    signal.signal(signal.SIGINT, self.shutdown) # ctrl + c
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse the socket
    self.serverSocket.bind(config['host'], config['bind_port']) # bind socket to host and port
    self.serverSocket.listen(10) # become server socket
    self.__clients = {}
    while True:
        (clientSocket, client_address) = self.serverSocket.accept() # establish connection
        d = threading.Thread(name = self.__getClientName(client_address), target = self.proxy_thread, args = (clientSocket, client_address))
        d.setDaemon(True)
        d.start()
        
# redirecting traffic
request = conn.recv(config['max_req_len']) # get request
fline = request.split('\n')[0] # parse 1st line
url = fline.split(' ')[1] # get url
httppos = url.find('://')# pos of ://
if (httppos==-1):
    temp=url
else:
    temp=url[(httppos+3):] # rst of url
portpos=temp.find(':') # pos of port, if any
webserverpos=temp.find('/') # find web server
if webserverpos ==-1:
    webserverpos=-len(temp)
webserver = ''
port=-1
if (portpos==-1 or webserverpos<portpos):
    port =80 # default port
    webserver=temp[:webserverpos]
else: # specific port
    port =int((temp[(portpos+1):])[:webserverpos-portpos-1])
    webserver=temp[:portpos]
    
#
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(config['time_out'])
s.connect((webserver, port))
s.sendall(request)

# receive
while 1: # True
    data = s.recv(config['max_req_len'])
    if (len(data)>0):
        conn.send(data) # send to browser/client
    else:
        break
