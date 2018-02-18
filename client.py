#!/usr/bin/env python
# -*- encoding: utf-8 -*-


# Python program to implement client side of chat room.
import socket
import select
import sys
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 4:
    print "Correct usage: script, IP address, port number, name"
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
Name = str(sys.argv[3])
server.connect((IP_address, Port))


def main():

	try: 
		while True:
		 
		    # maintains a list of possible input streams
		    sockets_list = [sys.stdin, server]
		 
		    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
		    
		    #If server send message to client, else, the client is typing a message to server
		    for socks in read_sockets:
			if socks == server:
			    message = socks.recv(2048)
			    print message
			    sys.stdout.write(Name+':')
			    sys.stdout.flush()
			else:
			    message = sys.stdin.readline()
			    server.send(Name+":"+message)
			    
		server.close()

	except KeyboardInterrupt:
			print "[*] Exiting program"
			server.close()
			return

if __name__ == "__main__":
	main()
