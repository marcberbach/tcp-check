#!/usr/bin/env python
import socket
import subprocess
import sys
import csv
import time
from datetime import datetime

while True :
	tofile = ('')
	with open ('tcp-check.txt') as csvfile:
		check = csv.reader(csvfile, delimiter=',')
		print ('\n'+(str(datetime.now())[0:19]))
		print ('===================')
		for row in check:
			remoteServerIP  = socket.gethostbyname(row[0])
			max=str(row).count(',')
			espaces = 30-len(row[0])
			try:
				i = 1
				screenprinting = (row[0]+ ' : '+ ' '*espaces + ' ')
				webprinting = '<font size="3"><u>' + (row[0]+ ' : '+ ' '*espaces + ' ') + '</u></font size>'
				fileline = screenprinting
				while i <= max :
					port = int(row[i]) 
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.settimeout(2.0)
					t1 = datetime.now()
					result = sock.connect_ex((remoteServerIP, port))
					spaces = (' '*(5-len(row[i])))
					if result == 0:
						result = str('TCP:{}'.format(port)+ spaces + 'is UP  ' + str(datetime.now()-t1)[6:11] + 's  ')
						webprinting = webprinting + '<font size="3" color=\"green\">' + result + '</font color>'
					else:
						result = str('TCP:{}'.format(port)+ spaces + 'is ** DOWN **  ')
						webprinting = webprinting + '<font size="3" color=\"red\">' + result + '</font color>'
					sock.close()
					screenprinting = screenprinting + result
					i +=1
				print (screenprinting)
				tofile += '<center><h1>' + webprinting + '</h1></center>\n'
				
			except KeyboardInterrupt:
				print ("You pressed Ctrl+C")
				sys.exit()

			except socket.gaierror:
				print ('Hostname could not be resolved. Exiting')
				sys.exit()

			except socket.error:
				print ("Couldn't connect to server")
				sys.exit()
	file = open('tcp-check-result.html', "w")
	header= ('<html>\n<head>\n<META HTTP-EQUIV="Refresh" CONTENT="3">\n</head>\n<body>\n')
	footer= ('</body>\n</html>\n')
	file.write(header + '<center><h1>'+ str(datetime.now())[0:19]+'  '+ '</h1></center>\n')
	file.write(tofile)
	file.write(footer)
	file.close()
	time.sleep(5)
