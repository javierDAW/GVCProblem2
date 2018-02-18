#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Python program to implement server side of chat room.
import socket
import select
import sys
import re

#Our functions
import externalFunctions as ef

from thread import *

 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
 
# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])
 
# takes second argument from command prompt as port number (Type 9200/tcp for this problem)
Port = int(sys.argv[2])
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))
 
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)
 
list_of_clients = []
 
def clientthread(conn, addr):
 
	# sends a message to the client whose user object is conn
	conn.send("Welcome to chatbot!")
 	first = True
	
	while True:
            try:
                message = conn.recv(2048)
                if message:
 
                    print addr[0] + ": " + message
 		    
                    # Calls broadcast function to send message to all
                    usr,act = filterMessage(message)
		    
		    """
		    Check if it is the first message, if so, check if the
		    message is a cordial greeting or matches a pattern
		    """

		    if first:
			#answer("Hi %s, how can I help you?"%usr, conn)
			resp = "Hi %s, how can I help you?"%usr
		    	first = False
		    	message_to_send = checkActions(act)	
			if(message_to_send != "No results found"):                  	
				resp = resp+"\n"+message_to_send
			answer(resp, conn)
		    else:
			message_to_send = checkActions(act)	
			answer(message_to_send, conn)
                else:
                    
                    remove(conn)
 
            except:
                continue

def filterMessage(msg):

	#Just in case the user sends ":" symbol in the message, we just analyze the first and the second one
	usr = msg.split(":")[0]
        act = msg.split(":")[1]
	return usr,act
	
 
"""
Open the file with rules and check if there are any match in there.
If it find some match, execute the command.
"""
def checkActions(act):

	with open("rules.config", "r") as f:
		data = f.readlines()
 
		for line in data:
			regex,action = line.split("::")
			m = re.match(regex,act, re.I)
			if m:
				if(re.match("FETCH_URL*",action)):
					return ef.fetchURL(action,m.group(1))
				elif(re.match("GREP*",action)):
					return ef.grep(action,m.group(1),m.group(2))
				elif(re.match("EXTERNAL*",action)):
					return ef.external(action,m.group(1))
	f.close()
	return "No results found"  


"""
Answer the client with proper results.
"""

def answer(message, connection):
	try:
                connection.send("Chatbot:"+message)
        except:
                connection.close()
 
                # if the link is broken, we remove the client
                remove(connection)

#Remove specific connection if it is necessary
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
 

def main():
	
	try:
		while True:
	 
		    	#Accepts a connection request and stores it
		    	conn, addr = server.accept()
		 
			#List of clients connected
		       	list_of_clients.append(conn)
		 
		    	# prints the address of the user that just connected
		    	print addr[0] + " connected"
		 
		    	# creates and individual thread for every user 
		    	# that connects
		    	start_new_thread(clientthread,(conn,addr))    
		 
		conn.close()
		server.close()
	
	except KeyboardInterrupt:
		print "[*] Exiting program"
		conn.close()
		server.close()
		return

if __name__ == "__main__":
	main()
