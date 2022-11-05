from mininet.topo import Topo


class NotAValidNumberOfSwitches(Exception):
    pass

class MyTopo(Topo):
    def __init__(self, number_of_switches : int):
        # Initialize topology
        Topo.__init__(self)

        if number_of_switches < 1:
            raise NotAValidNumberOfSwitches(str(number_of_switches) + " is not a valid number")
        

        # Create hosts
        h1 = self.addHost('host_1')
        h2 = self.addHost('host_2')
        h3 = self.addHost('host_3')
        h4 = self.addHost('host_4')

        # Create switches and add relationship with first hosts
        s1 = self.addSwitch('switch_0')
        self.addLink(s1,h1)
        self.addLink(s1,h2)

        s2 = None
        if number_of_switches == 1:
            s2 = s1
        else:
            for i in range(number_of_switches):
                s2 = self.addSwitch('switch_'+str(i))
                self.addLink(s1,s2)
                s1 = s2

        # Add relationship with last hosts
        self.addLink(s2,h3)
        self.addLink(s2,h4)


topos = {'customTopology': MyTopo}