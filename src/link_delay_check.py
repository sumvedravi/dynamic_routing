#!/usr/bin/python

import sys, re

from time import sleep

def main(argv):
	while True:
		if len(sys.argv) == 1:
			print("usage : delay_check.py <src host number> <dst host number>")
			sys.exit()
		str = '10.0.0.'
		src_host = argv[1]
		dst_host = argv[2]
		dst_host_ip = str + dst_host
		#print(dst_host_ip)
		print(dst_host_ip)

		import subprocess
		process = subprocess.Popen(['ping', '-c3', dst_host_ip ],
				     stdout=subprocess.PIPE, 
				     stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		print(stdout, stderr)
		stdout = stdout.decode("utf-8")
		# ping avg index is 4
		f = open('link_delay.log', 'a')
		f.write(src_host +" "+ dst_host+ " "+ stdout.split("/")[4] + "\n")
				
if __name__ == "__main__":
	main(sys.argv)
