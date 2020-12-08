from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from time import sleep

import sys
class nine_topo(Topo):

	def __init__(self):
		Topo.__init__(self)
		n = 9
		s = [ 'null_s' ]
		h = [ 'null_h' ]
		bw =    [100,100,  3,  1, 10,  5,100,  3,  3,  5,  1,  1,100,  1,  5,  3]
		delay = [  1,  1, 30,100, 50, 50,  1, 30, 30, 50,100,100,  1,100, 50, 30]

		for s_ind in range(n):
			s.append(self.addSwitch('s%s' % (s_ind + 1), dpid='000000000000000%s' % (s_ind + 1)))
		for h_ind in range(n):
			h.append(self.addHost('h%s' % (h_ind + 1)))


		self.addLink(s[1], s[2], bw = bw[0], delay = '%sms' % delay[0])
		self.addLink(s[2], s[3], bw = bw[1], delay = '%sms' % delay[1])
		self.addLink(s[1], s[4], bw = bw[2], delay = '%sms' % delay[2])
		self.addLink(s[1], s[5], bw = bw[3], delay = '%sms' % delay[3])
		self.addLink(s[2], s[5], bw = bw[4], delay = '%sms' % delay[4])
		self.addLink(s[2], s[6], bw = bw[5], delay = '%sms' % delay[5])
		self.addLink(s[3], s[6], bw = bw[6], delay = '%sms' % delay[6])
		self.addLink(s[4], s[5], bw = bw[7], delay = '%sms' % delay[7])
		self.addLink(s[5], s[6], bw = bw[8], delay = '%sms' % delay[8])
		self.addLink(s[4], s[7], bw = bw[9], delay = '%sms' % delay[9])
		self.addLink(s[4], s[8], bw = bw[10], delay = '%sms' % delay[10])
		self.addLink(s[5], s[8], bw = bw[11], delay = '%sms' % delay[11])
		self.addLink(s[5], s[9], bw = bw[12], delay = '%sms' % delay[12])
		self.addLink(s[6], s[9], bw = bw[13], delay = '%sms' % delay[13])
		self.addLink(s[7], s[8], bw = bw[14], delay = '%sms' % delay[14])
		self.addLink(s[8], s[9], bw = bw[15], delay = '%sms' % delay[15])

		self.addLink(s[1], h[1])
		self.addLink(s[2], h[2])
		self.addLink(s[3], h[3])
		self.addLink(s[4], h[4])
		self.addLink(s[5], h[5])
		self.addLink(s[6], h[6])
		self.addLink(s[7], h[7])
		self.addLink(s[8], h[8])
		self.addLink(s[9], h[9])
				
		#{dev type} {id} {dev type} {id} {bandwidth} {delay} 
		config_file = open('links.config', 'w')
		config_file.write('s 1 s 2 ' + str(bw[0]) + " " + str(delay[0]) + '\n')
		config_file.write('s 2 s 3 ' + str(bw[1]) + " " + str(delay[1]) + '\n')
		config_file.write('s 1 s 4 ' + str(bw[2]) + " " + str(delay[2]) + '\n')
		config_file.write('s 1 s 5 ' + str(bw[3]) + " " + str(delay[3]) + '\n')
		config_file.write('s 2 s 5 ' + str(bw[4]) + " " + str(delay[4]) + '\n')
		config_file.write('s 2 s 6 ' + str(bw[5]) + " " + str(delay[5]) + '\n')
		config_file.write('s 3 s 6 ' + str(bw[6]) + " " + str(delay[6]) + '\n')
		config_file.write('s 4 s 5 ' + str(bw[7]) + " " + str(delay[7]) + '\n')
		config_file.write('s 5 s 6 ' + str(bw[8]) + " " + str(delay[8]) + '\n')
		config_file.write('s 4 s 7 ' + str(bw[9]) + " " + str(delay[9]) + '\n')
		config_file.write('s 4 s 8 ' + str(bw[10]) + " " + str(delay[10]) + '\n') 
		config_file.write('s 5 s 8 ' + str(bw[11]) + " " + str(delay[11]) + '\n')
		config_file.write('s 5 s 9 ' + str(bw[12]) + " " + str(delay[12]) + '\n')
		config_file.write('s 6 s 6 ' + str(bw[13]) + " " + str(delay[13]) + '\n') 
		config_file.write('s 7 s 8 ' + str(bw[14]) + " " + str(delay[14]) + '\n')
		config_file.write('s 8 s 9 ' + str(bw[15]) + " " + str(delay[15]) + '\n')
		
		config_file.write('h 1 s 1 1 0\n')
		config_file.write('h 2 s 2 1 0\n')
		config_file.write('h 3 s 3 1 0\n')
		config_file.write('h 4 s 4 1 0\n')
		config_file.write('h 5 s 5 1 0\n')
		config_file.write('h 6 s 6 1 0\n')
		config_file.write('h 7 s 7 1 0\n')
		config_file.write('h 8 s 8 1 0\n')
		config_file.write('h 9 s 9 1 0\n')
		
		config_file.close()


if __name__ == '__main__':
	setLogLevel('info')
	topo = nine_topo()

	net = Mininet(topo=topo, controller=RemoteController("c0", ip="172.17.0.5"), link=TCLink, listenPort=None, autoSetMacs=True)

	net.start()
	h1, h2, h3, h4, h5, h6, h7, h8, h9 = net.get('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9')
	#s1, s2, s3 = net.get('s1', 's2', 's3')

	'''h1.cmd('python3 link_delay_check.py 1 2 &')
	h2.cmd('python3 link_delay_check.py 2 3 &')
	h1.cmd('python3 link_delay_check.py 1 4 &')
	h1.cmd('python3 link_delay_check.py 1 5 &')
	h2.cmd('python3 link_delay_check.py 2 5 &')
	h2.cmd('python3 link_delay_check.py 2 6 &')
	h3.cmd('python3 link_delay_check.py 3 6 &')
	h4.cmd('python3 link_delay_check.py 4 5 &')
	h5.cmd('python3 link_delay_check.py 5 6 &')
	h4.cmd('python3 link_delay_check.py 4 7 &')
	h4.cmd('python3 link_delay_check.py 4 8 &')
	h5.cmd('python3 link_delay_check.py 5 8 &')
	h5.cmd('python3 link_delay_check.py 5 9 &')
	h6.cmd('python3 link_delay_check.py 6 9 &')
	h7.cmd('python3 link_delay_check.py 7 8 &')
	h8.cmd('python3 link_delay_check.py 8 9 &')'''

	net.interact()

	net.stop()

	info("done!\n")
