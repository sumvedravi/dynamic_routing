#!/usr/bin/python

import sys, re, os
import subprocess

from time import sleep

def main(argv):
	if len(sys.argv) == 1:
		print("usage : delay_check.py <src host number> <dst host number>")
		sys.exit()
	str = '10.0.0.'
	while True:
		src_host = argv[1]
		dst_host = argv[2]
		dst_host_ip = str + dst_host
		#print(dst_host_ip)
		#print(dst_host_ip)

		stream = os.popen('ping -c3 ' + dst_host_ip)
		output = stream.read()
		#process = subprocess.Popen(['ping', '-c3', dst_host_ip ],
		#		     stdout=subprocess.PIPE, 
		#		     stderr=subprocess.PIPE)
		#stdout, stderr = process.communicate()
		#print(stdout, stderr)
		#stdout = stdout.decode("utf-8")
		# ping avg index is 4
		print(output)
		print(output.split("/"))
		if len(output.split("/")) != 7:
			continue
		f = open('../log/link_delay_' + src_host + '_' + dst_host + '.log', 'a')
		f.write(src_host +" "+ dst_host+ " "+ output.split("/")[4] + "\n")
		f.close()
				
if __name__ == "__main__":
	main(sys.argv)
