from socket import *
import ssl
import base64
import getpass


# Message to send
msg = '\r\nI love computer networks!'
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'
# Port number may change according to the mail server
mailPort = 465
# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
# Creating a SSL Wrapper to create a secure socket 
clientSocket = ssl.wrap_socket(clientSocket,      
                ssl_version=ssl.PROTOCOL_TLSv1,  
                ciphers="HIGH:-aNULL:-eNULL:-PSK:RC4-SHA:RC4-MD5",
                cert_reqs=ssl.CERT_REQUIRED,
		ca_certs = "/usr/local/lib/python2.7/dist-packages/certifi/cacert.pem")
# Connecting to the mail server
clientSocket.connect((mailserver, mailPort))
print("Connected")
recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
	print '220 reply not received from server.'

# Send HELO command and print server response.
heloCommand = 'HELO gmail.com\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
	print '250 reply not received from server.'

# Enter the username and password of your e mail
Username=raw_input("Insert Username: ")
Password= getpass.getpass(prompt='Insert Password: ')

# Encoding the string of username and password and Send Login Command.
LoginString=("\0"+Username+"\0"+Password).encode("base64")
print LoginString
LoginString= LoginString.strip("\n")
login = 'AUTH PLAIN '+ LoginString + '\r\n'
print login
clientSocket.send(login)
recv_login = clientSocket.recv(1024)
print recv_login


	
# Send MAIL FROM command and print server response.
mailfrom   = 'MAIL FROM: <'+ Username+'>\r\n'
print mailfrom
clientSocket.send(mailfrom)
recv2 = clientSocket.recv(1024)
print recv2
if recv2[:3] != '250':
    print '250 reply not received from server.'


# Send RCPT TO command and print server response. 
# Get input from user
receiver =raw_input("Send email to: ")
rcptto = 'RCPT TO: <'+ receiver +'>\r\n'
print rcptto
clientSocket.send(rcptto)
recv3 = clientSocket.recv(1024)
print recv3
if recv3[:3] != '250':
    print '250 reply not received from server.'

# Send DATA command and print server response. 
data = 'DATA\r\n'
print data
clientSocket.send(data)
recv4 = clientSocket.recv(1024)
print recv4
# Send message data with subject and msg and send Message ends with a single period.
Subject=raw_input("Subject: ")
clientSocket.send("Subject: "+Subject+msg+endmsg)
recv5 = clientSocket.recv(1024)
print recv5

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
clientSocket.send("QUIT\r\n")
recv6 = clientSocket.recv(1024)
print recv6
# Connection is closed
clientSocket.close()

