#!/usr/bin/python
# -*- coding: utf-8 -*-
#Redes 1 Trabalho Final 

from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, ether
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp
from ryu.lib import mac

import ryu.app.ofctl.api as api 
from ryu.app.wsgi import ControllerBase
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
import networkx as nx
#import matplotlib.pyplot as plt
import re
import itertools

ARP = arp.arp.__name__
IPV4 = ipv4.ipv4.__name__
ip_to_mac = { 
	'10.0.0.1' : '00:00:00:00:00:01',
	'10.0.0.2' : '00:00:00:00:00:02',
	'10.0.0.3' : '00:00:00:00:00:03',
	'10.0.0.4' : '00:00:00:00:00:04',
	'10.0.0.5' : '00:00:00:00:00:05',
	'10.0.0.99' : '00:00:00:00:00:99'
	}
#PoPs = [ '00:00:00:00:00:03',  '00:00:00:00:00:04', '00:00:00:00:00:05']
PoPs = { 
        '10.0.0.3': {'type': 'firewall','flows': [], 'status' : 'ok'},
        '10.0.0.4': {'type': 'firewall','flows': [], 'status' : 'bad'},
        '10.0.0.5': {'type': 'firewall','flows': [], 'status' : 'bad'}
       }
SFCs = { 
         '00:00:00:00:00:02':  ['00:00:00:00:00:03','00:00:00:00:00:02'],
         '00:00:00:00:00:01':  ['00:00:00:00:00:03','00:00:00:00:00:01'],
         '10.0.0.2':  ['firewall'],
         '10.0.0.1':  ['firewall']
       }
SFC_flows = {} 
class ProjectController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
 
    def __init__(self, *args, **kwargs):
        super(ProjectController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self
        self.net=nx.MultiDiGraph()
        self.nodes = {}
        self.links = {}
        self.no_of_nodes = 0
        self.no_of_links = 0
        self.i=0
  
    #Função para listar attributos no objeto
    def ls(self,obj):
        print("\n".join([x for x in dir(obj) if x[0] != "_"]))
    
    #Procurar protocolos num pacote
    def _find_protocol(self, pkt, name):
        for p in pkt.protocols:
            if hasattr(p, 'protocol_name'):
                if p.protocol_name == name:
                    return p

    #Pegar todos protocolos de um pacote
    def _get_protocols(self, pkt):
        protocols = {}
        for p in pkt:
            if hasattr(p, 'protocol_name'):
                protocols[p.protocol_name] = p
            else:
                protocols['payload'] = p
        return protocols

    #Função para responder ARP
    def send_arp(self, datapath, arp_opcode, src_mac, dst_mac, src_ip, dst_ip, arp_target_mac, in_port, output):
        ether_proto = ether.ETH_TYPE_ARP
        hwtype = 1
        arp_proto = ether.ETH_TYPE_IP
        hlen = 6
        plen = 4

        pkt = packet.Packet()
        e = ethernet.ethernet(dst_mac, src_mac, ether_proto)
        a = arp.arp(hwtype, arp_proto, hlen, plen, arp_opcode, src_mac, src_ip, arp_target_mac, dst_ip)
        pkt.add_protocol(e)
        pkt.add_protocol(a)
        pkt.serialize()

        actions = [datapath.ofproto_parser.OFPActionOutput(output)]
        datapath.send_packet_out(in_port=in_port, actions = actions, data=pkt.data)  
 
    def add_flow(self, datapath, match, actions, priority):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser      
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] 
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=priority, instructions=inst)
        datapath.send_msg(mod)

    def select_pop(self,pop_type):
        for pop in PoPs.keys():
            if PoPs[pop]['type'] == pop_type:
                best = pop
                if PoPs[pop]['status'] == 'ok':
                    return pop
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures , CONFIG_DISPATCHER)
    def switch_features_handler(self , ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS , actions)]
        mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, cookie=0,command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0, priority=0, instructions=inst)
        datapath.send_msg(mod)
 
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
 
        pkt = packet.Packet(msg.data)

        #Get protocols
        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4.ipv4)
        p_arp = pkt.get_protocol(arp.arp)

        #Ignore LLDP packets
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return
        
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        if src not in self.net:
            self.net.add_node(src)
            self.net.add_edge(dpid,src,port=in_port)
            self.net.add_edge(src,dpid)

        if p_arp:
            ipv4_src = ip.src if ip != None else p_arp.src_ip
            ipv4_dst = ip.dst if ip != None else p_arp.dst_ip
            target_mac = ip_to_mac[ipv4_dst]
            print "ARP!", ipv4_src, ipv4_dst
            self.send_arp(datapath, arp.ARP_REPLY, target_mac ,src, ipv4_dst, ipv4_src,src, ofproto.OFPP_CONTROLLER, in_port)
            return
       
        if dst in self.net:

            if ip != None and ip.dst in SFCs.keys():
                if (ip.dst,ip.src) in SFC_flows.keys():
                    print "Reflowing: DPID", dpid, ip.src, "->", ip.dst 
                    return
                else:
                    SFC_flows[(ip.dst,ip.src)] = []
                path_source = src
                whole_path = SFCs[ip.dst]
                whole_path.append(ip.dst)
                for pop in whole_path:
                    if pop == ip.dst:
                        path_target = ip_to_mac[pop]
                    else:
                        path_target = ip_to_mac[self.select_pop(pop)]
                    path=nx.shortest_path(self.net,path_source,path_target)  
                    SFC_flows[(ip.dst,ip.src)].append(path)
                    first = True
                    for i in path:
                        if isinstance(i,int):
                            switchDP = api.get_datapath(self, i)
                            next = path[path.index(i)+1]
                            pathes=self.net[i][next]
                            out_port=[pathes[p]['port'] for p in pathes if 'port' in pathes[p]][0]
                            actions = []
                            if first:
                                first = False
                                if path_source == src:
                                    first_packet_actions = [datapath.ofproto_parser.OFPActionSetField(ip_dscp=1), datapath.ofproto_parser.OFPActionOutput(out_port) ]
                                    actions.append(switchDP.ofproto_parser.OFPActionSetField(ip_dscp=1))
                                    match = switchDP.ofproto_parser.OFPMatch(eth_type=0x800,in_port=in_port, ipv4_src=ip.src,ipv4_dst=ip.dst)
                                else:
                                    match = switchDP.ofproto_parser.OFPMatch(eth_type=0x800,in_port=2, ipv4_src=ip.src,ipv4_dst=ip.dst,ip_dscp=1)
                                    #match correct in_port 
                            else:
                                match = switchDP.ofproto_parser.OFPMatch(eth_type=0x800,in_port=in_port, ipv4_src=ip.src,ipv4_dst=ip.dst,ip_dscp=1)
                            actions.append(switchDP.ofproto_parser.OFPActionOutput(out_port))
                            self.add_flow(switchDP, match, actions,2048)
                            #if next != dst: #Last of All
                            if next != path_target: #Last of segment
                                paths=self.net[next][i] #may not work for multiple connections between 2 switches
                                in_port=[paths[p]['port'] for p in paths if 'port' in paths[p]][0]
                            #    #add_flow
                            #else
                            #    #add_flow
                    path_source = path_target
                #print SFC_flows  

                out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,actions=first_packet_actions, data=msg.data)
                datapath.send_msg(out)
                return
            else:
                #Local hop mac redirection (non-SFC traffic)
                print "b:", dst 
                path=nx.shortest_path(self.net,src,dst)  
                next=path[path.index(dpid)+1]
                paths=self.net[dpid][next]
                out_port=[paths[p]['port'] for p in paths if 'port' in paths[p]][0]

                match = datapath.ofproto_parser.OFPMatch(eth_type=0x800,in_port=in_port, eth_dst=dst)
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, match, actions,2048)

                print "  path: ", path
                print "  outport: ", out_port
                print "  next: ", next
                print "  dpid: ", dpid
                #print self.net.edges(data=True, keys=True)
                out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,actions=actions, data=msg.data)

                datapath.send_msg(out)
   
    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self.topology_api_app, None)  
        switches=[switch.dp.id for switch in switch_list]
        self.net.add_nodes_from(switches)
       
        links_list = get_link(self.topology_api_app, None)
        #print links_list
        #links=[(link.src.dpid,link.dst.dpid,port=link.src.port_no) for link in links_list]
        #print links
        #self.net.add_edges_from(links)
        #links=[(link.dst.dpid,link.src.dpid,port=link.dst.port_no) for link in links_list]
        #print links
        #self.net.add_edges_from(links)
        for link in links_list:
            if (link.src.dpid,link.dst.dpid,link.src.port_no) not in list(self.net.edges_iter(data='port')):
                self.net.add_edge(link.src.dpid,link.dst.dpid,port=link.src.port_no)
            if (link.dst.dpid,link.src.dpid,link.dst.port_no) not in list(self.net.edges_iter(data='port')):
                self.net.add_edge(link.dst.dpid,link.src.dpid,port=link.dst.port_no)

