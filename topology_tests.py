import unittest
from topology import ChainTopo, InvalidNumberOfSwitches

class TestAlbum(unittest.TestCase):
    def test_WhenGivenThreeSwitchesItShouldReturnATopologyWithThreeSwitches(self):
        topology = ChainTopo(number_of_switches = 3)
        assert len(topology.switches()) == 3
        assert len(topology.hosts()) == 4

    def test_WhenGivenTenSwitchesItShouldReturnATopologyWithTenSwitches(self):
        topology = ChainTopo(number_of_switches = 10)
        assert len(topology.switches()) == 10
        assert len(topology.hosts()) == 4

    def test_WhenGivenZeroSwitchesItShouldRaiseAnException(self):
        with self.assertRaises(InvalidNumberOfSwitches):
            ChainTopo(number_of_switches = 0)

    def test_WhenGivenTwoSwitchesItShouldReturnATopologyWithTwoSwitches(self):
        topology = ChainTopo(number_of_switches = 2)
        assert len(topology.switches()) == 2
        assert len(topology.hosts()) == 4


if __name__ == '__main__':
    unittest.main()
