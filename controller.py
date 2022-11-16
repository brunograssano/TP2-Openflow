from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import json

# Add your imports here ...
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt

log = core.getLogger()

# Add your global variables here ...
IP = 0x0800

class Firewall(EventMixin) :
    def __init__ ( self ) :
        self.listenTo(core.openflow)
        config = self.read_config("rules.json")
        self.firewall_switch = config["firewall_switch"]
        log.debug("Enabling Firewall Module")
    
    def _handle_ConnectionUp(self, event):
        if event.dpid == self.firewall_switch:
            self.block_port(event, 80)
            self.block_by(event, "10.0.0.1", 5001, "TCP")
            self.block_communication_between(event, "10.0.0.2", "10.0.0.3")
            log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

    def block_port(self, event, port):
        ''' Blocks all incoming packets to `port` number '''

        # Mathes incoming packets that has port as port destination
        portMatch = of.ofp_match()
        portMatch.dl_type = IP
        portMatch.nw_proto = pkt.ipv4.TCP_PROTOCOL
        portMatch.tp_dst = port

        # Changes routing table so that those packets are dropped
        msg = of.ofp_flow_mod()
        msg.match = portMatch
        event.connection.send(msg)

        portMatch = of.ofp_match()
        portMatch.dl_type = IP
        portMatch.nw_proto = pkt.ipv4.UDP_PROTOCOL
        portMatch.tp_dst = port

        msg = of.ofp_flow_mod()
        msg.match = portMatch
        event.connection.send(msg)

        log.debug("Firewall block port %d rule installed on %s", port, dpidToStr(event.dpid))

    def block_by(self, event, host, to_port, with_protocol):
        ''' Blocks all incoming packets from `host` to `port` number `with_protocol` '''

        hostToPortWithProtocolMatch = of.ofp_match()
        hostToPortWithProtocolMatch.dl_type = IP
        hostToPortWithProtocolMatch.nw_src = IPAddr(host)
        hostToPortWithProtocolMatch.tp_dst = to_port
        hostToPortWithProtocolMatch.nw_proto = pkt.ipv4.TCP_PROTOCOL if with_protocol == "TCP" else pkt.IPV4.UDP_PROTOCOL

        msg = of.ofp_flow_mod()
        msg.match = hostToPortWithProtocolMatch
        event.connection.send(msg)

        log.debug("Firewall block host %s to port %d with protocol %s rule installed on %s", host, to_port, with_protocol, dpidToStr(event.dpid))

    def block_communication_between(self, event, host1, host2):
        ''' Blocks all communication packets between `host1` and `host2` '''

        host1ToHost2Match = of.ofp_match()
        host1ToHost2Match.dl_type = IP
        host1ToHost2Match.nw_src = IPAddr(host1)
        host1ToHost2Match.nw_dst = IPAddr(host2)

        msg = of.ofp_flow_mod()
        msg.match = host1ToHost2Match
        event.connection.send(msg)

        host2ToHost1Match = host1ToHost2Match.flip()

        msg = of.ofp_flow_mod()
        msg.match = host2ToHost1Match
        event.connection.send(msg)

        log.debug("Firewall block communication with %s and %s rule installed on %s", host1, host2, dpidToStr(event.dpid))

    def read_config(self, config_file):
        f = open (config_file, "r")
        config = json.loads(f.read())
        f.close()
        return config

def launch():
    # Starting the Firewall module
    core.registerNew(Firewall)
