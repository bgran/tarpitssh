#
#
#
import asyncore
import time
import socket

class SSHClientHandler(asyncore.dispatcher):
    def fixate_buffers(self, sock):
        state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        #print(f"SO_RCVBUF: old {state}")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        new_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        #print(f"SO_RCVBUF: new {new_state}")

        state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        #print(f"SO_SNDBUF: old {state}")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1)
        state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        #print(f"SO_SNDBUF: new {state}")
    def __init__(self, sock, addr, port):
        asyncore.dispatcher.__init__(self, sock)
        self.fixate_buffers(sock)
        self.addr = addr
        self.port = port
        ssh_version = "SSH-2.0-OpenSSH_8.4p1 Debian-5+deb11u1\r\n"
        self.buffer = []
        for s in ssh_version[::-1]:
            s = s.encode()
            self.buffer.append(s)
        self.start = self.timer = time.time()
        self._readable = True
    def handle_read(self):
        t1 = time.time()
        data = self.recv(1024)
        if not data:
            #self.handle_close()
            self.close()
            #print(f"Wasted {t1-self.start} seconds of {self.addr}:{self.port} time")
    def readable(self):
        return self._readable
    def writable(self):
        buffer_rem = len(self.buffer) > 0
        if not buffer_rem:
            self.handle_close()
        else:
            times = time.time()
            tdiff = (times - self.timer) > 3.0
            if tdiff:
                self.timer = times
                return True
            else:
                return False
    def handle_write(self):
        assert len(self.buffer) > 0, "self.buffer len is 0 or less"
        sent = self.send(self.buffer.pop()) 
        if sent == 0:
            print(f"sent {sent} bytes")
            self.handle_close()
    def handle_close(self):
        t1 = time.time()
        self._readable = False
        self.close()
        tbl = asyncore.socket_map
        print(f"Wasted {t1-self.start} seconds of {self.addr}:{self.port} time")
class SSHServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1023)
    def handle_accepted(self, sock, addr):
        print(f"New connecion from {addr}")
        SSHClientHandler(sock, addr[0], addr[1])
def run():
    server = SSHServer("0.0.0.0", 8022)
    running = True
    while running:
        #print(f"Socket_map: {asyncore.socket_map}")
        asyncore.poll2(1.0)

