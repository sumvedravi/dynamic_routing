from config import *
from onos_interface import *
from onos_topo import *
from time import sleep

import sys, re, os
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
from sklearn import preprocessing



def check_portstats(stats, links, graph):
	print("[info] check portstats")
	# get max bw per links
	
	# file merge
	os.system('cat ../log/link_delay_* > ../log/link_delay.log')
	
	for src_dev in stats:
		for src_port in stats[src_dev]:	
			curr_bw = (stats[src_dev][src_port]['bytesRx'] + \
				stats[src_dev][src_port]['bytesTx']) * 8 / 1000 / 1000
			for dst_dev in links[src_dev]:
				if links[src_dev][dst_dev]['src_port'] == src_port:
					max_bw = links[src_dev][dst_dev]['max_bw']
					bw_per_sec = max(curr_bw - links[src_dev][dst_dev]['bw_before'], 0)
					links[src_dev][dst_dev]['bw_before'] = curr_bw
					links[src_dev][dst_dev]['bw'] = bw_per_sec / max_bw
					print('[info] src ' + src_dev + ' dst ' + dst_dev + ' bw collected')
					# onos portstat show only network devices' ports stats
					# use h->s stats with the same value s->h
					if dst_dev[0:2] != 'of':
						links[dst_dev][src_dev]['bw_before'] = curr_bw
						links[dst_dev][src_dev]['bw'] = bw_per_sec / max_bw
						print('[info] src ' + src_dev + ' dst ' + dst_dev + 'bw collected')
	
					# get delay	
					# helper script : link_check_delay.py h1 s1
					for line in reversed(list(open("../log/link_delay.log"))):
						line = line.rstrip()
						line_src_dev = line.split(" ")[0]
						line_dst_dev = line.split(" ")[1]
						line_delay = line.split(" ")[2]
						# device and switch should be no more than 10.
						if line_src_dev[0:1] == 's':
							line_src_dev = 'of:000000000000000' + line_src_dev[1:2]
						else:
							line_src_dev = '00:00:00:00:00:0' + line_src_dev[1:2]
						if line_dst_dev[0:1] == 's':
							line_dst_dev = 'of:000000000000000' + line_dst_dev[1:2]
						else:
							line_dst_dev = '00:00:00:00:00:0' + line_dst_dev[1:2]
						if line_src_dev == src_dev and line_dst_dev == dst_dev:
							links[dst_dev][src_dev]['delay'] = line_delay
							links[src_dev][dst_dev]['delay'] = line_delay
							print('[info] src ' + src_dev + ' dst ' + dst_dev + 'delay collected')
							break

	# caculate normalized value 
	bw_norm = []
	delay_norm = []
	for src in links:
		for dst in links[src]:
			if links[src][dst]['bw'] != -1:
				bw_norm.append( links[src][dst]['bw'] )
			if links[src][dst]['delay'] != -1:
				delay_norm.append( links[src][dst]['delay'] )
	bw_norm = preprocessing.normalize([bw_norm])[0]
	delay_norm = preprocessing.normalize([delay_norm])[0]
	bw_norm_ind = 0
	delay_norm_ind = 0
	for src in links:
		for dst in links[src]:
			if links[src][dst]['bw'] != -1:
				links[src][dst]['bw_norm'] = bw_norm[bw_norm_ind]
				bw_norm_ind += 1
			if links[src][dst]['delay'] != -1:
				links[src][dst]['delay_norm'] = delay_norm[delay_norm_ind]
				delay_norm_ind += 1
				

	# calculate efficiency per link
	alpha = 1
	beta = 2
	gamma = 0.25
	for src in links:
		for dst in links[src]:
			if links[src][dst]['delay_norm'] != -1 and links[src][dst]['bw_norm'] != -1:
				links[src][dst]['efficency'] = alpha * links[src][dst]['bw_norm'] * \
					gamma * links[src][dst]['link_flow_count'] + \
					beta * links[src][dst]['delay_norm']
				print('[info] src ' + src +  ' dst ' + dst + ' link efficency updated')
				graph[src][dst]['weight'] = links[src][dst]['efficency']	
