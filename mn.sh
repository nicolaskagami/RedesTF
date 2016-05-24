#mn --topo single,3 --mac --switch ovsk,protocols=OpenFlow13 --controller remote
mn --custom Mininet/topology.py --topo TFTopo --mac --switch ovsk,protocols=OpenFlow13 --controller remote
#mn --custom topology.py --topo TFTopo --mac --switch ovsk,protocols=OpenFlow13
