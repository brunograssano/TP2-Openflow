import unittest
from topology import MyTopo, NotAValidNumberOfSwitches

class TestAlbum(unittest.TestCase):
    def test_WhenGivenThreeSwitchesItShouldReturnATopologyWithThreeSwitches(self):
        topology = MyTopo(number_of_switches = 3)
        assert len(topology.switches()) == 3
        assert len(topology.hosts()) == 4

    def test_WhenGivenTenSwitchesItShouldReturnATopologyWithTenSwitches(self):
        topology = MyTopo(number_of_switches = 10)
        assert len(topology.switches()) == 10
        assert len(topology.hosts()) == 4

    def test_WhenGivenZeroSwitchesItShouldRaiseAnException(self):
        with self.assertRaises(NotAValidNumberOfSwitches):
            MyTopo(number_of_switches = 0)

    def test_WhenGivenTwoSwitchesItShouldReturnATopologyWithTwoSwitches(self):
        topology = MyTopo(number_of_switches = 2)
        assert len(topology.switches()) == 2
        assert len(topology.hosts()) == 4


if __name__ == '__main__':
    unittest.main()
