import socket

def sendjason():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = "10.0.20.35"
    port = 7011
    try:
        #s.connect((ip, port))
        #s.send(updatejasonstr.encode())
        s.sendto("123".encode(), (ip, port))
        s.close()
    except Exception as e:
        print("send erro to : ip "+ip+" port "+str(port)+" "+str(e))
        s.close()
    return

if __name__ == '__main__':
    sendjason()