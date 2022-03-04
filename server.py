import socket
import cv2
import pickle
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#Defines the Address Family & Socket type (TCP in this case)
host_name = socket.gethostname()		#Grabs name of host machine
host_ip = socket.gethostbyname(host_name)  	#Grabs IP of the host machine

print("HOST IP: ", host_ip)

port = 9999				#Open port that will be used
socket_address = (host_ip, port)	

server_socket.bind(socket_address)	

server_socket.listen(5)			#Listens on the selected port for a connection request, arg is for maximum allowed connections
print("LISTENING AT: ", socket_address)

while True:
	client_socket, addr = server_socket.accept()		#Accepts connection from the client machine
	print('GOT CONNECTION FROM', addr)
	if client_socket:
		vid = cv2.VideoCapture(0)			#Chooses webcam to use, 0 is default, -1 may be used if having trouble finding a webcam
		while((vid.isOpened)):
			img, frame = vid.read()			#Reads the information from 
			a = pickle.dumps(frame)			#Turns object 'frame' into a 'bytes' object
			message = struct.pack("Q", len(a))+a	#Turns 'a' into a string representation
			client_socket.sendall(message)
			cv2.imshow('TRANSMITTING VIDEO', frame) #Shows the video stream
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				client_socket.close()
	
