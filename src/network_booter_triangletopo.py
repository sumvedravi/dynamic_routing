from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from time import sleep

import sys
class triangle_topo(Topo):

	def __init__(self):
		Topo.__init__(self)

		s1 = self.addSwitch('s1', dpid='0000000000000001')
		s2 = self.addSwitch('s2', dpid='0000000000000002')
		s3 = self.addSwitch('s3', dpid='0000000000000003')

		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')

		self.addLink(s1, s2, bw = 1, delay = '100ms')
		self.addLink(s2, s3, bw = 10, delay = '1ms')
		self.addLink(s1, s3, bw = 10, delay = '1ms')

		self.addLink(s1, h1)
		self.addLink(s2, h2)
		self.addLink(s3, h3)
				
		config_file = open('links.config', 'w')
		config_file.write('s 1 s 2 1 100\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.write('s 2 s 3 10 1\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.write('s 1 s 3 10 1\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.write('h 1 s 1 1 0\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.write('h 2 s 2 1 0\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.write('h 3 s 3 1 0\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.close()


#topos = { 'triangle': triangle_topo }

if __name__ == '__main__':
	setLogLevel('info')
	topo = triangle_topo()

	net = Mininet(topo=topo, controller=RemoteController("c0", ip="172.17.0.5"), link=TCLink, listenPort=None, autoSetMacs=True)

	net.start()
	h1, h2, h3 = net.get('h1', 'h2', 'h3')
	s1, s2, s3 = net.get('s1', 's2', 's3')

	'''h1.cmd('python3 link_delay_check.py 1 2 &')
	h1.cmd('python3 link_delay_check.py 1 3 &')
	h2.cmd('python3 link_delay_check.py 2 1 &')
	h2.cmd('python3 link_delay_check.py 2 3 &')
	h3.cmd('python3 link_delay_check.py 3 1 &')
	h3.cmd('python3 link_delay_check.py 3 2 &')'''

	net.interact()

	net.stop()

	info("done!\n")
