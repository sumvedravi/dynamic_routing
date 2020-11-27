from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from mininet.link import TCLink

def topology():

	net = Mininet(controller=RemoteController, link = TCLink)

	s1 = net.addSwitch('s1', dpid='0000000000000001')
	s2 = net.addSwitch('s2', dpid='0000000000000002')
	s3 = net.addSwitch('s3', dpid='0000000000000003')

	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	h3 = net.addHost('h3')

	c1 = net.addController(name ='c1', controller=RemoteController, ip='172.15.0.5', port=6653)

	a = net.addLink(s1, s2, bw = 10)#, delay = rand())
	net.addLink(s2, s3, bw = 10)
	net.addLink(s1, s3, bw = 10)

	net.addLink(s1, h1)
	net.addLink(s2, h2)
	net.addLink(s3, h3)

	net.build()
	c1.start()
	s1.start([c1])
	s2.start([c1])
	s3.start([c1])

	net.start()

	CLI(net)
	
	net.stop()

if __name__ == '__main__':
	topology()

