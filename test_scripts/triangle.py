from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from mininet.link import TCLink

class TriangleTopo(Topo):
	
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

		f1 = open('net.conf', 'w')
		f1.write('hi u dope')
		f1.write('second line')
		f1.close()

topos = { 'triangle': TriangleTopo }
