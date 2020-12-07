#!/usr/bin/python

import sys, re, os
import subprocess

from time import sleep

def main(argv):
	if len(sys.argv) == 1:
		print("usage : delay_check.py <src dev> <dst dev>")
		print("usage : delay_check.py s1 s2")
		sys.exit()
	ip_pfx = '10.0.0.'
	src_dev_str = argv[1]
	dst_dev_str = argv[2]
	src_dev_no = int(argv[1][1:])
	dst_dev_no = int(argv[2][1:])
	dst_dev_ip = ip_pfx + str(dst_dev_no)
	while True:

		stream = os.popen('ping -c3 ' + dst_dev_ip)
		output = stream.read()

		# ping avg index is 4
		print(output)
		print(output.split("/"))
		# validation out and skip invalid form 
		if len(output.split("/")) != 7:
			continue
		f = open('../log/link_delay_' + src_dev_str + '_' + dst_dev_str + '.log', 'a')
		f.write(src_dev_str +" "+ dst_dev_str + " "+ output.split("/")[4] + "\n")
		f.close()
				
if __name__ == "__main__":
	main(sys.argv)
