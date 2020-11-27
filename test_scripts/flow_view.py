from mininet.topo import Topo


class TriangleTopo(Topo):
	
	def __init__(self):
		Topo.__init__(self)

		s1 = self.addSwitch('s1', dpid='0000000000000001')
		s2 = self.addSwitch('s2', dpid='0000000000000002')
		s3 = self.addSwitch('s3', dpid='0000000000000003')

		h1 = self.addHost('h1')
		h2 = self.addHost('h2')

		#self.addLink(s1, s2)
		#self.addLink(s2, s3)

		self.addLink(s1, h1)
		self.addLink(s3, h2)


topos = { 'triangle': (lambda: TriangleTopo()) }

