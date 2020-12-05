from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from time import sleep

class linear_topology(Topo):
	
	def __init__(self):
		Topo.__init__(self)

		s1 = self.addSwitch('s1', dpid='0000000000000001')
		s2 = self.addSwitch('s2', dpid='0000000000000002')
		#s3 = self.addSwitch('s3', dpid='0000000000000003')

		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		#h3 = self.addHost('h3')

		self.addLink(s1, s2, bw = 10, delay = '10ms')
		#self.addLink(s2, s3, bw = 10, delay = '10ms')
		#self.addLink(s1, s3, bw = 10, delay = '10ms')

		self.addLink(s1, h1)
		self.addLink(s2, h2)
		#self.addLink(s3, h3)

		config_file = open('links.config', 'w')

		config_file.write('s 1 s 2 10 10\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.write('h 1 s 1 -1 0\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file.write('h 2 s 2 -1 0\n') 	#{dev type} {id} {dev type} {id} {bandwidth} {delay} 

		# update link delay dynamically
		config_file.close()

		

topos = { 'linear-test': linear_topology }

if __name__ == '__main__':
	#setLogLevel('debug')
	setLogLevel('info')
	topo = linear_topology()

	net = Mininet(topo=topo, controller=RemoteController("c0", ip="172.17.0.5"), link=TCLink, listenPort=None, autoSetMacs=True)

	net.start()
	h1, h2 = net.get('h1', 'h2')
	s1, s2 = net.get('s1', 's2')

	h1.cmd('python3 link_delay_check.py 1 2 &')
	h2.cmd('python3 link_delay_check.py 2 1 &')
	#h2.cmd('ping 10.0.0.2')

	#s1.cmd('ip addr add 10.0.0.101/24 brd + dev lo')
	s1.setIP('10.0.0.101', intf = 'lo')
	s2.setIP('10.0.0.102', intf = 'lo')
	net.interact()

	net.stop()

	info("done!\n")

