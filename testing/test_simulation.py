import unittest

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution
from neatbots.organism import Organism

class Test_Simulation(unittest.TestCase):

    def setUp(self):
        self.test_sim = Simulation("./voxcraft-sim/voxcraft-sim", "./voxcraft-sim/vx3_node_worker", "./generations", heap_size=0.6)
        self.test_evo = Evolution(self.test_sim, 1, 1, 1, 1, 1)
        self.test_orgs = self.test_evo.construct_organisms(0)

    # Simulation class exists
    def test_sim_exists(self):
        self.assertIsNotNone(self.test_sim)


if __name__ == "__main__":
    unittest.main()
