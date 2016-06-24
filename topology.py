#!/usr/bin/python
# coding=utf-8

import time
from mininet.topo import Topo
from mininet.net import Containernet
from mininet.node import RemoteController, Host, OVSKernelSwitch, OVSSwitch, Docker
from mininet.util import dumpNodeConnections
from mininet.link import TCLink, Link
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from subprocess import call

pop_cpu_percentage=15
pop_link_bw=3
def tfTopo():
    net = Containernet( topo=None, controller=RemoteController, switch=OVSKernelSwitch )

    net.addController( 'c0', RemoteController, ip="127.0.0.1", port=6633 )

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
    p2 = net.addHost('p2', ip='10.0.1.2', mac='00:00:00:00:01:02', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=5000)
    p3 = net.addHost('p3', ip='10.0.1.3', mac='00:00:00:00:01:03', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=5000)
    p4 = net.addHost('p4', ip='10.0.1.4', mac='00:00:00:00:01:04', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=5000)
    p5 = net.addHost('p5', ip='10.0.1.5', mac='00:00:00:00:01:05', cls=Docker, dimage='gmiotto/click',mem_limit=1024*1024*10, cpu_quota=pop_cpu_percentage*100,cpu_period=5000)

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
    net.addLink(p1,s1, cls=TCLink, delay="100ms",bw=pop_link_bw,loss=0)
    net.addLink(p1,s1)

    net.addLink(p2,s2, cls=TCLink, delay="100ms",bw=pop_link_bw,loss=0)
    net.addLink(p2,s2)

    net.addLink(p3,s3, cls=TCLink, delay="100ms",bw=pop_link_bw,loss=0)
    net.addLink(p3,s3)

    net.addLink(p4,s4, cls=TCLink, delay="100ms",bw=pop_link_bw,loss=0)
    net.addLink(p4,s4)

    net.addLink(p5,s5, cls=TCLink, delay="100ms",bw=pop_link_bw,loss=0)
    net.addLink(p5,s5)

    #Normal Hosts
    net.addLink(h1,s1)
    net.addLink(h2,s2)
    net.addLink(h3,s3)
    net.addLink(h4,s4)
    net.addLink(h5,s5)
    net.addLink(h6,s6)
    net.addLink(h7,s7)
    net.addLink(h8,s8)
    net.addLink(h9,s9)
    net.addLink(h10,s10)

    net.addLink(s7, s1) #s7-s1
    net.addLink(s7, s2) 
    net.addLink(s1, s2) 
    net.addLink(s1, s8) 
    net.addLink(s1, s3) 
    net.addLink(s1, s6) 
    net.addLink(s8, s3) 
    net.addLink(s2, s5) 
    net.addLink(s2, s4) 
    net.addLink(s3, s5) 
    net.addLink(s3, s4) 
    net.addLink(s4, s9) 
    net.addLink(s4, s6) 
    net.addLink(s5, s6) 
    net.addLink(s5, s10) 
    net.addLink(s9, s6) 
    net.addLink(s10, s6) 

    #net.addLink(s6, s3, cls=TCLink, delay="100ms", bw=0.5, loss=0)

    net.start()

    for host in net.hosts:
        if "h" in host.name:
            host.cmd('ethtool -K %s-eth0 tso off' % host.name)
            host.cmd('python httpserver.py  80 &')

    for host in net.hosts:
        if "p" in host.name:
            call("sudo bash Click/runFirewall.sh %s Click/firewall3.click " % host.name,shell=True)

    time.sleep(10)
            
    #h1.cmd('bash client.sh "h1" &')
    #h3.cmd('bash client.sh "h3" &')
    for host in net.hosts:
        if "h" in host.name and host.name != "h2":
            print host.name
            host.cmd('bash client.sh %s &' % host.name)
    #call("sudo bash Click/runFirewall.sh h4 Click/firewall3.click ",shell=True)
    #call("sudo bash Click/runFirewall.sh h5 Click/firewall3.click ",shell=True)

    time.sleep(150)
    #h1.cmd('echo ha')
    #h3.cmd('echo ha')
    #time.sleep(150)
    for host in net.hosts:
        if "h" in host.name:
            host.cmd('echo ha')

    #CLI(net)
    net.stop()

if __name__ == '__main__':
   setLogLevel( 'info' )
   tfTopo()