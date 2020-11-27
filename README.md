# dynamic_routing
ONOS + Mininet Simulated Network Architecture with Dynamic Routing Protocol 


# Program Start-Up
start up onos cluster  
start up onos gui  

$ cd ~/onos-app-samples/ifwd  
$ onos-app 172.17.0.5 install! ./target/onos-app-ifwd-1.9.0-SNAPSHOT.oar   
$ onos  
$ onos> apps -a -s  
$ onos> app deactivate org.onosproject.fwd  
$ onos> app activate org.onosproject.ifwd  
$ onos> app activate org.onosproject.metrics  
$ onos> app activate org.onosproject.imr  
$ onos> apps -a -s   
$ onos> imr:startmon {app id of imr} org.onosproject.ifwd  
$ onos> logout  
  
$ cd ~/workspace/dynamic_routing/src  
$ sudo mn --custom network_booter.py --topo linear-test --controller remote,172.17.0.5 --nolistenport --mac --link=tc  
  
  
$ python3 main.py  
