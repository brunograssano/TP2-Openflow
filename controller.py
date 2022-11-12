from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

# Add your imports here ...
from pox.lib.addresses import IPAddr

log = core.getLogger()

# Add your global variables here ...

class Firewall(EventMixin) :
    def __init__ ( self ) :
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
    
    def _handle_ConnectionUp(self, event):
        # Add your logic here ...
        my_match = of.ofp_match()
        my_match.nw_dst = IPAddr("10.00.00.01")
        my_match.tp_dst = 80

        msg = of.ofp_flow_mod()
        msg.match = my_match

        event.connection.send(msg)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    # Starting the Firewall module
    core.registerNew(Firewall)
