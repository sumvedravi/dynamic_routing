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
		s3 = self.addSwitch('s3', dpid='0000000000000003')

		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')

		a = self.addLink(s1, s2, bw = 10)#, delay = rand())
		self.addLink(s2, s3, bw = 10)
		self.addLink(s1, s3, bw = 10)

		self.addLink(s1, h1)
		self.addLink(s2, h2)
		self.addLink(s3, h3)


topos = { 'triangle': TriangleTopo }

if __name__ == '__main__':
	topo = TriangleTopo()

	net = Mininet(topo=topo, \
			controller=RemoteController(name = 'c1', ip ='172.17.0.5'), \
			link = TCLink)

	net.start()

	CLI(net)
	
	net.stop()