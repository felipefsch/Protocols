To make it properly works, first get familiar with mininet and openflow framework.

After running the initial tutorial of POX as remote controller for mininet, just overwrite the file
<path_to_pox>/pox/misc/of_tutorial.py. Now the controller provided here will be the controller of your
SDN.

Starting the controller:
cd <path_to_pox>
./pox.py log.level --DEBUG misc.of_tutorial
sudo mn --topo single,3 --mac --switch ovsk --controller=remote,ip=192.168.0.102

Note: this implementation assumes you are using the flag --mac while starting mininet.
Also, you must set the remote ip as the IP from br0 interface of the host computer.


Important links:
-mininet walktrhough: http://mininet.org/walkthrough/
-openflow and pox: http://archive.openflow.org/wk/index.php/OpenFlow_Tutorial#Controller_Choice:_POX_.28Python.29
-pox: https://openflow.stanford.edu/display/ONL/POX+Wiki#POXWiki-OpenFlowinPOX
-pox learning switches: https://github.com/mininet/openflow-tutorial/wiki/Create-a-Learning-Switch