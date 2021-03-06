import os, shutil, subprocess
from typing import List

from lxml import etree
from neatbots.VoxcraftVXA import VXA
from neatbots.VoxcraftVXD import VXD

class Simulation():
    """Contains all methods and properties relevant to simulating voxel-based organisms."""

    def __init__(self, exec_path: os.path, node_path: os.path, stor_path: os.path, heap_size: float, sim_time: float):
        """Constructs a Simulation object.

        Args:
            exec_path (os.path): Relative path for the 'voxcraft-sim' executable
            node_path (os.path): Relative path for the 'vx3_node_worker' executable
            stor_path (os.path): Relative path for the result files to be stored within
            heap_size (float): Percentage of GPU heap available for simulation use
            sim_time (float): Duration of simulation process

        Returns:
            (Simulation): Simulation object with the specified arguments 
        """

        # Create absolute paths for simulation execution
        self.exec_path = exec_path
        self.node_path = node_path
        self.stor_path = stor_path

        # Clear the storage directory
        self.empty_directory(self.stor_path)

        # Configure simulation settings
        self.vxa = VXA(HeapSize=heap_size, SimTime=sim_time, EnableExpansion=1, TempEnabled=1, VaryTempEnabled=1, TempPeriod=0.1, TempBase=25, TempAmplitude=20)

        # Define material types
        self.materials = [
                            0, # empty
                            self.vxa.add_material(RGBA=(0,255,0), E=1e9, RHO=1e3), # passive
                            self.vxa.add_material(RGBA=(255,0,0), E=1e7, RHO=1e6, CTE=0.01) # active
                         ]

    def encode_morphology(self, morphology: List[int], generation_path: os.path, label: str, id: int, step_size: int = 0):
        """Encodes a 3D array of integers as an XML tree describing a soft-body robot and writes it as a .vxd file.

        Args:
            morphology (List[int]): 3D array of integers
            generation_path (os.path): Absolute path for storing encodings
            label (str): General filename for encodings
            id (int): Unique filename for encodings
            step_size (int, optional): Number of timesteps to record. Defaults to 0
        """
        
        # Settings for simulated individual
        vxd = VXD()
        vxd.set_tags(RecordStepSize=step_size)
        vxd.set_data(morphology)
        vxd.write(os.path.join(generation_path, label + "_" + str(id) + ".vxd"))

    def empty_directory(self, target_path: os.path):
        """Empties a directory completely.

        Args:
            target_path (os.path): Absolute path to the directory to empty
        """

        for root, dirs, files in os.walk(target_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def store_generation(self, generation_dir: str):
        """Creates a directory and stores the simulation settings within.

        Args:
            generation_dir (str): Relative path of the directory to create

        Returns:
            (os.path): Absolute path to the newly created directory
        """

        # Make storage directory if not already made
        gene_path = os.path.join(self.stor_path, generation_dir)
        os.makedirs(gene_path, exist_ok=True)
        # Ensure directory is empty
        self.empty_directory(gene_path)
        # Store simulation settings and materials
        self.vxa.write(os.path.join(gene_path, "base.vxa"))

        return gene_path

    def simulate_generation(self, generation_path: os.path):
        """Runs a VoxCraft-Sim simulation with the specified settings and inputs.

        Args:
            generation_path (os.path): Absolute path for storing settings and results

        Returns:
           (Dict[str, int]): Dictionary of id-fitness pairs describing organism performance
           (str): String containing an XML-like structure for VoxCraft-Viz to visualise
        """

        # Run voxcraft-sim as subprocess 
        voxcraft_out = subprocess.run([self.exec_path,
                                      '-i', generation_path, 
                                      '-o', os.path.join(generation_path, "results.xml"), 
                                      '-w', self.node_path,
                                      '--force'], 
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        
        
        # Return fitness scores
        with open(os.path.join(generation_path, "results.xml"), 'r') as f:
            tree = etree.parse(f)
            
        # Pair organisms with their fitnesses
        fitnesses = {str(r.tag).split("_")[1]: float(r.xpath("fitness_score")[0].text) for r in tree.xpath("//detail/*")}

        # Parse hsitory
        history = voxcraft_out.stdout.decode('utf-8')

        return fitnesses, history

