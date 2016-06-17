# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 
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
from ryu.topology.api import get_switch, get_link
from ryu.app.wsgi import ControllerBase
from ryu.topology import event, switches
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
PoPs = [ '00:00:00:00:00:03' ]
SFCs = { 
         '00:00:00:00:00:04':  ('00:00:00:00:00:03')
       }
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
  
    # Handy function that lists all attributes in the given object
    def ls(self,obj):
        print("\n".join([x for x in dir(obj) if x[0] != "_"]))

    def add_sfc_flow(self, datapath, dst, actions, sfcId):
        print "Adding SFC flow", datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser      
        match = datapath.ofproto_parser.OFPMatch(eth_type=0x0800,ip_dscp=sfcId , eth_dst=dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] 
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY, instructions=inst)
        datapath.send_msg(mod)

    def add_first_flow(self, datapath,in_port, dst, actions):
        print "Adding SFC flow", datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser      
        match = datapath.ofproto_parser.OFPMatch(eth_type=0x0800, in_port=in_port, eth_dst=dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] 
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY, instructions=inst)
        datapath.send_msg(mod)

    def add_sfc_pop_flow(self, datapath, in_port, dst, actions, sfcId):
        print "Adding SFC flow PoP: ", datapath.id, in_port
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser      
        match = datapath.ofproto_parser.OFPMatch(eth_type=0x0800,ip_dscp=sfcId,in_port=in_port, eth_dst=dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] 
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY+1, instructions=inst)
        datapath.send_msg(mod)
 
    def add_flow(self, datapath, in_port, dst, actions):
        print "Adding flow"
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser      
        match = datapath.ofproto_parser.OFPMatch(eth_type=0x800,in_port=in_port, eth_dst=dst)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] 
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY, instructions=inst)
        datapath.send_msg(mod)
 
    def _find_protocol(self, pkt, name):
        for p in pkt.protocols:
            if hasattr(p, 'protocol_name'):
                if p.protocol_name == name:
                    return p

    def _get_protocols(self, pkt):
        protocols = {}
        for p in pkt:
            if hasattr(p, 'protocol_name'):
                protocols[p.protocol_name] = p
            else:
                protocols['payload'] = p
        return protocols

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures , CONFIG_DISPATCHER)
    def switch_features_handler(self , ev):
         #print "switch_features_handler is called"
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
        eth = pkt.get_protocol(ethernet.ethernet)
 
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        #p_arp = self._find_protocol(pkt, "arp")

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
	   # print "lldp"
            # ignore lldp packet
            return

        ip = pkt.get_protocol(ipv4.ipv4)

        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        #print "nodes"
        #print self.net.nodes()
        #print "edges"
        #print self.net.edges()


        p_arp = pkt.get_protocol(arp.arp)
        if p_arp:
            ipv4_src = ip.src if ip != None else p_arp.src_ip
            ipv4_dst = ip.dst if ip != None else p_arp.dst_ip
            target_mac = ip_to_mac[ipv4_dst]
            print "ARP!", ipv4_src, ipv4_dst
            self.send_arp(datapath, arp.ARP_REPLY, target_mac ,src, ipv4_dst, ipv4_src,src, ofproto.OFPP_CONTROLLER, in_port)
            return
       
            
        if src not in self.net:
            #print "1 Src:", src
            self.net.add_node(src)
            self.net.add_edge(dpid,src,port=in_port)
            self.net.add_edge(src,dpid)
        if dst in self.net:
            #print "2"
            if dst in SFCs.keys() and ip != None:
                #path=(nx.shortest_path(self.net,src,SFCs[dst]), nx.shortest_path(self.net,SFCs[dst],dst))  
                #Tag the flow!
                #if dpid == 3:
                #    if in_port == 2:
                #actions = [
                #           datapath.ofproto_parser.OFPActionSetField(ip_dscp=0),
                #           datapath.ofproto_parser.OFPActionOutput(out_port)
                #          ]
                #self.add_sfc_flow(datapath, in_port, dst, actions,0)
                #if dpid == 3:
                #    actions = [
                #               datapath.ofproto_parser.OFPActionSetField(ip_dscp=1),
                #               datapath.ofproto_parser.OFPActionOutput(out_port)
                #              ]
                #    self.add_sfc_flow(datapath, in_port, dst, actions,0)

                #actions = [
                #           datapath.ofproto_parser.OFPActionSetField(ip_dscp=0),
                #           datapath.ofproto_parser.OFPActionOutput(out_port)
                #          ]
                #self.add_flow(datapath, in_port, dst, actions)
                

                path=nx.shortest_path(self.net,src,SFCs[dst])  
                print path
                for i in path:
                    if isinstance(i,int):
                        switchDP = api.get_datapath(self, i)
                        #switchId = switchDP.id
                        next = path[path.index(i)+1]
                        pathes=self.net[i][next]
                        out_port=[pathes[p]['port'] for p in pathes if 'port' in pathes[p]][0]
                        #out_port = self.net[i][next][0]['port']
                        print i, out_port, next
                        if i == dpid:
                            print "First"
                            actions = [
                                       switchDP.ofproto_parser.OFPActionSetField(ip_dscp=0),
                                       switchDP.ofproto_parser.OFPActionOutput(out_port)
                                      ]
                            self.add_first_flow(datapath,in_port, dst, actions)
                            out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,actions=actions, data=msg.data)
                        elif next == SFCs[dst]:
                            print "next"
                            actions = [
                                switchDP.ofproto_parser.OFPActionSetField(ip_dscp=1),
                                switchDP.ofproto_parser.OFPActionOutput(1)
                                      ]
                            self.add_sfc_pop_flow(switchDP, 3, dst, actions,0)

                        else:
                            actions = [
                                       #switchDP.ofproto_parser.OFPActionSetField(ip_dscp=0),
                                       switchDP.ofproto_parser.OFPActionOutput(out_port)
                                      ]
                            self.add_sfc_flow(switchDP, dst, actions,0)
                            
                        last = i

                print "POP: ", last
                actions = [
                           switchDP.ofproto_parser.OFPActionSetField(ip_dscp=1),
                           switchDP.ofproto_parser.OFPActionOutput(4)
                          ]
                self.add_sfc_pop_flow(switchDP, 2, dst, actions,1)
                

                path=nx.shortest_path(self.net,SFCs[dst],dst)  
                #path=nx.shortest_path(self.net,src,dst)  
                for i in path:
                    if isinstance(i,int) and i != last:
                        switchDP = api.get_datapath(self, i)
                        #switchId = switchDP.id
                        next = path[path.index(i)+1]
                        pathes=self.net[i][next]
                        out_port=[pathes[p]['port'] for p in pathes if 'port' in pathes[p]][0]
                        #out_port = self.net[i][next][0]['port']
                        print i, out_port, next
                        if next == dst:
                            actions = [
                                       switchDP.ofproto_parser.OFPActionSetField(ip_dscp=0),
                                       switchDP.ofproto_parser.OFPActionOutput(out_port)
                                      ]
                            self.add_sfc_flow(switchDP, dst, actions,1)
                        else:
                            actions = [
                                       switchDP.ofproto_parser.OFPActionOutput(out_port)
                                      ]
                            self.add_sfc_flow(switchDP, dst, actions,1)
                        #self.add_flow_debug(switchDP, dst, actions)
                datapath.send_msg(out)
                return
            else:
                print "b:", dst 
                path=nx.shortest_path(self.net,src,dst)  
                next=path[path.index(dpid)+1]
                pathes=self.net[dpid][next]
                out_port=[pathes[p]['port'] for p in pathes if 'port' in pathes[p]][0]
                #out_port=self.net[dpid][next][0]['port']
            #path=nx.shortest_path(self.net,src,'00:00:00:00:00:03')  
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                self.add_flow(datapath, in_port, dst, actions)

            print "  path: ", path
            print "  outport: ", out_port
            print "  next: ", next
            print "  dpid: ", dpid
            #print self.net.edges(data=True, keys=True)
        else:
            #print "3"
            out_port = ofproto.OFPP_FLOOD
            return
 
        # install a flow to avoid packet_in next time
        #if out_port != ofproto.OFPP_FLOOD:
        #    self.add_flow(datapath, in_port, dst, actions)
 
        out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,actions=actions, data=msg.data)

        datapath.send_msg(out)
   
    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self.topology_api_app, None)  
        switches=[switch.dp.id for switch in switch_list]
        self.net.add_nodes_from(switches)
        
        #print "**********List of switches"
        #for switch in switch_list:
          #self.ls(switch)
          #print switch
        #  self.nodes[self.no_of_nodes] = switch
        #  self.no_of_nodes += 1
       
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
        print "List of links"
        print self.net.edges(data=True, keys=True)
        #nx.draw(self.net);
        #plt.show();

    def send_arp(self, datapath, arp_opcode, src_mac, dst_mac,
                 src_ip, dst_ip, arp_target_mac, in_port, output):
        # Generate ARP packet
        ether_proto = ether.ETH_TYPE_ARP
        hwtype = 1
        arp_proto = ether.ETH_TYPE_IP
        hlen = 6
        plen = 4

        pkt = packet.Packet()
        e = ethernet.ethernet(dst_mac, src_mac, ether_proto)
        a = arp.arp(hwtype, arp_proto, hlen, plen, arp_opcode,
                    src_mac, src_ip, arp_target_mac, dst_ip)
        pkt.add_protocol(e)
        pkt.add_protocol(a)
        pkt.serialize()

        actions = [datapath.ofproto_parser.OFPActionOutput(output)]
        datapath.send_packet_out(in_port=in_port, actions = actions, data=pkt.data)  
	print pkt

