import unittest
import tracemalloc
import torch
import pandas as pd
import numpy as np
import plotly.express as px
from analytics.continuum_modelling.microkinetic_modelling import MicroKineticModel, OxygenReductionModel, ECpD
from analytics.materials.electrolytes import Electrolyte
from analytics.materials.solutes import Solute, MolecularOxygen
from analytics.materials.ions import Cation, Anion
from analytics.materials.solvents import Solvent
from analytics.materials.polymers import NType


class TestMicrokinetic(unittest.TestCase):

    na_cation = Cation(name='Na+')
    cl_anion = Anion(name='Cl-')
    water_solvent = Solvent('water')
    oxygen_solute = MolecularOxygen()

    my_electrolye = Electrolyte(solvent=water_solvent, 
                                cation=na_cation, 
                                anion=cl_anion, 
                                concentrations={na_cation: 0.1, cl_anion: 0.1, oxygen_solute: 0.00025}, 
                                solute=oxygen_solute, 
                                pH=7, 
                                temperature=298)
    
    my_polymer = NType('BBL')

    def test_electrolyte(self):
        self.assertTrue(self.my_electrolye.pH == 7)
        self.assertTrue(self.my_electrolye.temperature == 298)
        self.assertTrue(self.my_electrolye.solvent.name == 'Water')
        self.assertTrue(self.my_electrolye.cation.name == 'Sodium')
        self.assertTrue(self.my_electrolye.anion.name == 'Chloride')
        self.assertTrue(self.my_electrolye.solute.name == 'Oxygen')
        self.assertTrue(self.my_electrolye.cation.formula == 'NA+')
        self.assertTrue(self.my_electrolye.anion.formula == 'CL-')
        self.assertTrue(self.my_electrolye.solvent.formula == 'H2O')
        self.assertTrue(self.my_electrolye.concentrations[self.na_cation] == 0.1)
        self.assertTrue(self.my_electrolye.concentrations[self.cl_anion] == 0.1)
        self.assertTrue(self.my_electrolye.concentrations[self.oxygen_solute] == 0.00025)

    def test_polymer(self):
        self.assertTrue(self.my_polymer.name == 'BBL')

    my_microkinetic_model = MicroKineticModel(electrolyte=my_electrolye, polymer=my_polymer, rotation_rate=1600)

    def test_microkinetic_model_attributes(self):
        self.assertTrue(self.my_microkinetic_model.pH == 7)
        self.assertTrue(self.my_microkinetic_model.rotation_rate == 1600)
        self.assertTrue(self.my_microkinetic_model.temperature == 298)
        self.assertTrue(self.my_microkinetic_model.cation == self.na_cation)
        self.assertTrue(self.my_microkinetic_model.anion == self.cl_anion)
        self.assertTrue(self.my_microkinetic_model.solvent == self.water_solvent)


class TestOrrModel(unittest.TestCase):

    my_polymer = NType('BBL')

    na_cation = Cation(name='Na+')
    cl_anion = Anion(name='Cl-')
    water_solvent = Solvent('water')
    oxygen_solute = MolecularOxygen()

    def test_orr_model(self):

        my_electrolye = Electrolyte(solvent=self.water_solvent, 
                                    cation=self.na_cation, 
                                    anion=self.cl_anion, 
                                    concentrations={self.na_cation: 0.1, self.cl_anion: 0.1, self.oxygen_solute: 0.00025}, 
                                    solute=self.oxygen_solute, 
                                    pH=7, 
                                    temperature=298,
                                    diffusivities={self.oxygen_solute: 0.000019},
                                    viscosity=0.01)

        my_ORR_model = OxygenReductionModel(electrolyte=my_electrolye, polymer=self.my_polymer, rotation_rate=1600)
        self.assertTrue(my_ORR_model.pH == 7)
        self.assertTrue(my_ORR_model.rotation_rate == 1600)
        self.assertTrue(my_ORR_model.temperature == 298)
        self.assertTrue(my_ORR_model.cation == self.na_cation)
        self.assertTrue(my_ORR_model.anion == self.cl_anion)
        self.assertTrue(my_ORR_model.solvent == self.water_solvent)
        self.assertTrue(my_ORR_model.solute == self.oxygen_solute)
        self.assertTrue(my_ORR_model.x == 2)
        self.assertTrue(my_ORR_model.diffusivities[self.oxygen_solute] == 0.000019)
        self.assertTrue(my_ORR_model.viscosity == 0.01)
        self.assertTrue(round(my_ORR_model.diffusion_layer_thickness, 4) == 0.0015)
        self.assertTrue(round(my_ORR_model._o2._diffusion_layer_thickness, 4) == 0.0015)
        self.assertTrue(round(my_ORR_model.mass_transfer_coefficient, 4) == 0.0123)

    def test_orr_low_pH(self):

        my_electrolye = Electrolyte(solvent=self.water_solvent, 
                                    cation=self.na_cation, 
                                    anion=self.cl_anion, 
                                    concentrations={self.na_cation: 0.1, self.cl_anion: 0.1, self.oxygen_solute: 0.00025}, 
                                    solute=self.oxygen_solute, 
                                    pH=0, 
                                    temperature=298,
                                    diffusivities={self.oxygen_solute: 0.000019},
                                    viscosity=0.01)

        my_ORR_model = OxygenReductionModel(electrolyte=my_electrolye, polymer=self.my_polymer, rotation_rate=1600)
        self.assertTrue(my_ORR_model.x == 0)
        self.assertTrue(type(my_ORR_model.o2 == MolecularOxygen))

    def test_orr_high_pH(self):

        my_electrolye = Electrolyte(solvent=self.water_solvent, 
                                    cation=self.na_cation, 
                                    anion=self.cl_anion, 
                                    concentrations={self.na_cation: 0.1, self.cl_anion: 0.1, self.oxygen_solute: 0.00025}, 
                                    solute=self.oxygen_solute, 
                                    pH=14, 
                                    temperature=298,
                                    diffusivities={self.oxygen_solute: 0.000019},
                                    viscosity=0.01)

        my_ORR_model = OxygenReductionModel(electrolyte=my_electrolye, polymer=self.my_polymer, rotation_rate=1600)
        self.assertTrue(my_ORR_model.x == 1)

    def test_orr_invalid_pH(self):

        my_electrolye = Electrolyte(solvent=self.water_solvent, 
                                    cation=self.na_cation, 
                                    anion=self.cl_anion, 
                                    concentrations={self.na_cation: 0.1, self.cl_anion: 0.1, self.oxygen_solute: 0.00025}, 
                                    solute=self.oxygen_solute, 
                                    pH=20, 
                                    temperature=298,
                                    diffusivities={self.oxygen_solute: 0.000019},
                                    viscosity=0.01)

        with self.assertRaises(ValueError):
            my_ORR_model = OxygenReductionModel(electrolyte=my_electrolye, polymer=self.my_polymer, rotation_rate=1600)

    def test_orr_invalid_pH_2(self):

        my_electrolye = Electrolyte(solvent=self.water_solvent, 
                                    cation=self.na_cation, 
                                    anion=self.cl_anion, 
                                    concentrations={self.na_cation: 0.1, self.cl_anion: 0.1, self.oxygen_solute: 0.00025}, 
                                    solute=self.oxygen_solute, 
                                    pH=-3, 
                                    temperature=298,
                                    diffusivities={self.oxygen_solute: 0.000019},
                                    viscosity=0.01)

        with self.assertRaises(ValueError):
            my_ORR_model = OxygenReductionModel(electrolyte=my_electrolye, polymer=self.my_polymer, rotation_rate=1600)


class TestECpDModel(unittest.TestCase):

    na_cation = Cation(name='Na+')
    cl_anion = Anion(name='Cl-')
    water_solvent = Solvent('water')
    oxygen_solute = MolecularOxygen()

    my_electrolye = Electrolyte(solvent=water_solvent, 
                                cation=na_cation, 
                                anion=cl_anion, 
                                concentrations={na_cation: 0.1, cl_anion: 0.1, oxygen_solute: 0.0008}, 
                                solute=oxygen_solute, 
                                pH=14.2, 
                                temperature=298,
                                diffusivities={oxygen_solute: 0.000019},
                                viscosity=0.01
                                )
    
    my_polymer = NType('BBL')

    def test_ECpD_model(self):

        my_ECpD_model = ECpD(electrolyte=self.my_electrolye, polymer=self.my_polymer, rotation_rate=1600)
        self.assertTrue(my_ECpD_model.pH == 14.2)
        self.assertTrue(my_ECpD_model.rotation_rate == 1600)
        self.assertTrue(my_ECpD_model.temperature == 298)
        self.assertTrue(my_ECpD_model.cation == self.na_cation)
        self.assertTrue(my_ECpD_model.anion == self.cl_anion)
        self.assertTrue(my_ECpD_model.solvent == self.water_solvent)
        self.assertTrue(my_ECpD_model.solute == self.oxygen_solute)
        self.assertTrue(my_ECpD_model.x == 1)

    def test_k3_calculation(self):

        my_ECpD_model = ECpD(electrolyte=self.my_electrolye, polymer=self.my_polymer, rotation_rate=1600)
        k3 = my_ECpD_model.calculate_k3()
        k3 = round(k3, 0)
        self.assertTrue(k3 == 16380)

    def test_solve_parameters(self):

        my_polymer = NType('BBL', formal_reduction_potential=-0.3159)
        my_ECpD_model = ECpD(electrolyte=self.my_electrolye, polymer=my_polymer, rotation_rate=1600)

        parameters = my_ECpD_model.solve_parameters(E=0.7, k01=np.exp(-5.906), beta=0.4999, kf2=np.exp(1.0807), kf3=np.exp(4.688))
        self.assertTrue(type(parameters) == dict)

    def test_get_e_sweep(self):

        my_polymer = NType('BBL', formal_reduction_potential=-0.3159)
        my_ECpD_model = ECpD(electrolyte=self.my_electrolye, polymer=my_polymer, rotation_rate=1600)

        e_sweep = my_ECpD_model.get_e_sweep(E_max=1, E_min=-1, E_n=100, k01=np.exp(-5.906), beta=0.4999, kf2=np.exp(1.0807), kf3=np.exp(4.688))
        # px.line(e_sweep, x='potential', y='CS02_superoxide').show()
        self.assertTrue(type(e_sweep) == pd.DataFrame)
