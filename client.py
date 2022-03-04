import socket
import cv2
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.249'
port = 9999

client_socket.connect((host_ip, port))
data = b""

payload_size = struct.calcsize("Q")

while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024)	#reads the received packet in maximum 4096 byte increments
		if not packet: 				#if packet returns 0, loop ends
			break
		data += packet				#appends packet to data
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q", packed_msg_size)[0]	#determines the size of the message being received
	
	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	frame_data = data[:msg_size]			#takes the first msg_size elements from data
	data = data[msg_size:]				#removes the last msg_size elements from data
	frame = pickle.loads(frame_data)		#turns bytes object into frame object
	cv2.imshow("Received", frame)			#Shows the frame
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break

client_socket.close()
	
