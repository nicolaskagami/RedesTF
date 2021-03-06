#!/usr/bin/python
# coding=utf-8

from mininet.topo import Topo
from mininet.net import Containernet
from mininet.node import RemoteController, Host, OVSKernelSwitch, OVSSwitch, Docker
from mininet.util import dumpNodeConnections
from mininet.link import TCLink, Link
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from subprocess import call

import sys
import getopt
import time
import random

#Parameters
pop_cpu_percentage=10
pop_link_bw=100
pop_link_loss=0
pop_link_delay="0ms"

inter_switch_bw=100
inter_switch_loss=0
inter_switch_delay="1ms"

host_switch_bw=1
host_switch_loss=0
host_switch_delay="1ms"

def tfTopo():
    net = Containernet( topo=None, controller=RemoteController, switch=OVSKernelSwitch )

    net.addController( 'c0', RemoteController, ip="127.0.0.1", port=6633 )

    #Arguments
    opts, args = getopt.getopt(sys.argv[1:], "", ["flows=", "dos="])
    for o, a in opts:
        if o == "--flows":
            number_of_flows=int(a)
            print "Flows: ",a
        elif o in ("--dos"):
            number_of_dos=int(a)
            print "DoS: ",a

# Hosts 
    h1 = net.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', ip='10.0.0.3', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')
    h5 = net.addHost('h5', ip='10.0.0.5', mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', ip='10.0.0.6', mac='00:00:00:00:00:06')
    h7 = net.addHost('h7', ip='10.0.0.7', mac='00:00:00:00:00:07')
    h8 = net.addHost('h8', ip='10.0.0.8', mac='00:00:00:00:00:08')
    h9 = net.addHost('h9', ip='10.0.0.9', mac='00:00:00:00:00:09')
    h10 = net.addHost('h10', ip='10.0.0.10', mac='00:00:00:00:00:10')

    p1 = net.addHost('p1', ip='10.0.1.1', mac='00:00:00:00:01:01', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=10000)
    p2 = net.addHost('p2', ip='10.0.1.2', mac='00:00:00:00:01:02', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=10000)
    p3 = net.addHost('p3', ip='10.0.1.3', mac='00:00:00:00:01:03', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=10000)
    p4 = net.addHost('p4', ip='10.0.1.4', mac='00:00:00:00:01:04', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=10000)
    p5 = net.addHost('p5', ip='10.0.1.5', mac='00:00:00:00:01:05', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=10000)
    p6 = net.addHost('p6', ip='10.0.1.6', mac='00:00:00:00:01:06', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=10000)

    #Switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    s7 = net.addSwitch('s7')
    s8 = net.addSwitch('s8')
    s9 = net.addSwitch('s9')
    s10 = net.addSwitch('s10')

    #PoP Hosts
    net.addLink(p1,s1, cls=TCLink, delay=pop_link_delay,bw=pop_link_bw,loss=pop_link_loss)
    net.addLink(p1,s1)

    net.addLink(p2,s2, cls=TCLink, delay=pop_link_delay,bw=pop_link_bw,loss=pop_link_loss)
    net.addLink(p2,s2)

    net.addLink(p3,s3, cls=TCLink, delay=pop_link_delay,bw=pop_link_bw,loss=pop_link_loss)
    net.addLink(p3,s3)

    net.addLink(p4,s4, cls=TCLink, delay=pop_link_delay,bw=pop_link_bw,loss=pop_link_loss)
    net.addLink(p4,s4)

    net.addLink(p5,s5, cls=TCLink, delay=pop_link_delay,bw=pop_link_bw,loss=pop_link_loss)
    net.addLink(p5,s5)

    net.addLink(p6,s6, cls=TCLink, delay=pop_link_delay,bw=pop_link_bw,loss=pop_link_loss)
    net.addLink(p6,s6)

    #Normal Hosts
    net.addLink(h1,s1, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h2,s2, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h3,s3, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h4,s4, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h5,s5, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h6,s6, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h7,s7, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h8,s8, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h9,s9, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)
    net.addLink(h10,s10, cls=TCLink, delay=host_switch_delay,bw=host_switch_bw,loss=host_switch_loss)

    net.addLink(s7, s1, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) #s7-s1
    net.addLink(s7, s2, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s1, s2, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s1, s8, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s1, s3, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s1, s6, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s8, s3, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s2, s5, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s2, s4, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s3, s5, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s3, s4, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s4, s9, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s4, s6, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s5, s6, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s5, s10, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s9, s6, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 
    net.addLink(s10, s6, cls=TCLink, delay=inter_switch_delay,bw=inter_switch_bw,loss=inter_switch_loss) 

    net.start()

    for host in net.hosts:
        if "h" in host.name:
            host.cmd('ethtool -K %s-eth0 tso off' % host.name)
            host.cmd('python httpserver.py  80 &')

    for host in net.hosts:
        if "p" in host.name:
            call("sudo bash Click/runFirewall.sh %s Click/firewall3.click " % host.name,shell=True)


    CLI(net)
    net.stop()

if __name__ == '__main__':
   setLogLevel( 'info' )
   tfTopo()
