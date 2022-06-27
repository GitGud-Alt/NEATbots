import numpy as np

from neatbots.simulation import Simulation
from neatbots.evolution import Evolution

def main():
    main_sim = Simulation(heap_size=0.5)
    main_evo = Evolution(main_sim, 1, 5)

    main_evo.evolve()

if __name__ == "__main__":
    main()

# Run simulation only
# ./neatbots/voxcraft/voxcraft-sim -i ./neatbots/voxcraft/generation -o ./neatbots/voxcraft/generation/results.xml -w ./neatbots/voxcraft/vx3_node_worker -f