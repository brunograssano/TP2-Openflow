from mininet.topo import Topo


class InvalidNumberOfSwitches(Exception):
    pass

class ChainTopo(Topo):
    def __init__(self, number_of_switches):
        # Initialize topology
        Topo.__init__(self)

        if number_of_switches < 1:
            raise InvalidNumberOfSwitches(str(number_of_switches) + " is not a valid number")
        

        # Create hosts
        h1 = self.addHost('host_1')
        h2 = self.addHost('host_2')
        h3 = self.addHost('host_3')
        h4 = self.addHost('host_4')

        # Create switches and add relationship with first hosts
        s1 = self.addSwitch('switch_1')
        self.addLink(s1,h1)
        self.addLink(s1,h2)

        s2 = None
        if number_of_switches == 1:
            s2 = s1
        else:
            for i in range(2, number_of_switches + 1):
                s2 = self.addSwitch('switch_'+str(i))
                self.addLink(s1,s2)
                s1 = s2

        # Add relationship with last hosts
        self.addLink(s2,h3)
        self.addLink(s2,h4)


topos = {'chain': ChainTopo}
