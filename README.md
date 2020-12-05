# prerequsite
ONOS at least 3.0.8  
Mininet at least 2.3.0d6  
Linux OS(at least Ubuntu 16.04.7 LTS)  
Pacakges : python3-matplotlib, networkx
  sudo apt-get install python3-matplotlib  
  sudo apt install python3-pip
  sudo pip3 install networkx
  
# dynamic_routing
ONOS + Mininet Simulated Network Architecture with Dynamic Routing Protocol 


# Program Start-Up
start up onos cluster  
start up onos gui  

$ cd ~/onos-app-samples/ifwd  
$ onos-app 172.17.0.5 install! ./target/onos-app-ifwd-1.9.0-SNAPSHOT.oar   
$ onos 172.17.0.5 

$ onos> apps -a -s  
$ onos> app deactivate org.onosproject.fwd  
$ onos> app activate org.onosproject.ifwd  
$ onos> app activate org.onosproject.metrics  
$ onos> app activate org.onosproject.imr  
$ onos> apps -a -s   
$ onos> imr:startmon {app id of imr} org.onosproject.ifwd  
$ onos> logout  
  
$ cd ~/workspace/dynamic_routing/src  
$ sudo python network_booter.py 
$ mininet> pingall  

New Terminal:
$ cd ~/workspace/dynamic_routing/src    
$ python3 main.py  


# Additional Information

The '--mac' parameter is included so that each host device maintains easy mac id's to read numbered starting from 0.
Though this is a nice feature, it is no longer needed since the program is no longer static bound to mac id's.  

The 'link=tclink' is needed to allow the topology to set up bandwidth and link delays. These bw and delay 
parameters should be assigned randomly (or statically for testing). The network_booter.py file holds a very basic
topology which can be tested. 


