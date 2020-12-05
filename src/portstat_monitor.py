from config import *
from onos_interface import *
from onos_topo import *
from time import sleep


import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

import re


def portstat_check(hosts, devices, links, graph):
	before_bw = 0
	#format [(dev id, flow id, port no, type, src mac, dst mac, out port, out type), ...]
	print(links)
	stats = get_stats()
	pprint(stats)
	# get max bw per links
	ind = -1
	for link in links:
		ind = ind + 1
		if (link[0] == 'switch-switch'):
			src_sw = 's' + re.findall('\d+', link[1])[0].lstrip('0') + '-' + str(link[2])
			dest_sw = 's' + re.findall('\d+', link[3])[0].lstrip('0') + '-' + str(link[4])
			max_bw = link[4] * 1000 * 1000
			#print(typeof(stats))
			curr_bw = (stats[link[1]][link[2]]['bytesRx'] + stats[link[1]][link[2]]['bytesTx']) / 8
			print(src_sw, dest_sw, max_bw, curr_bw)
			links[ind][7] = curr_bw / 1000000 - links[ind][7]

	# get current bw per links
	# 
	# get delay
	# is the delay value custom? or 

'''for host in hosts_dict:
                host_mac = host['mac']
                dst_dev = host['locations'][0]['elementId']
                dst_port = int(host['locations'][0]['port'] )

                bandwidth, delay = find_config_match(links_config, ['h', 's'], [host_mac, dst_dev])

                links.append( ('host-switch', host_mac, -1, dst_dev, dst_port, bandwidth, delay) )

                hosts.append(host_mac)


        for dev in devs_dict:
                dev_id = dev['id']
                devices.append(dev_id)

        for link in links_dict:
                dst_dev = link['dst']['device']
                dst_port = int(link['dst']['port'])
                src_dev = link['src']['device']
                src_port = int(link['src']['port'])

                bandwidth, delay = find_config_match(links_config, ['s', 's'], [src_dev, dst_dev])

                links.append( ('switch-switch', src_dev, src_port, dst_dev, dst_port, bandwidth, delay) )

        devices = list(set(devices))
        links= list(set(links))

        for host in hosts:
                graph.add_node(host, type='host')
        for device in devices:
                graph.add_node(device, type='device')
        for link in links:
                graph.add_edge(link[1], link[3], weight = 1.0) #can add weight based on delay

'''
