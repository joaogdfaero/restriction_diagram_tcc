# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 19:23:41 2022

@author: FSRENTAL
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
from ADRpy import unitconversions as co
from ADRpy import constraintanalysis as ca
from ADRpy import atmospheres as at

designatm = at.Atmosphere()

designbrief = {'rwyelevation_m':co.feet2m(295), 'groundrun_m':90, # <- Take-off requirements
               'stloadfactor': 2.5, 'turnalt_m': 1000, 'turnspeed_ktas': 70, # <- Turn requirements
               'climbalt_m': 1500, 'climbspeed_kias': 50, 'climbrate_fpm': 1000, # <- Climb requirements
               'cruisealt_m': 0, 'cruisespeed_ktas': 110, 'cruisethrustfact': 1.0, # <- Cruise requirements
               'servceil_m': 15000, 'secclimbspd_kias': 50, # <- Service ceiling requirements
               'vstallclean_kcas': 38} # <- Required clean stall speed

TOW_kg = 450

designdefinition = {'aspectratio':7.43, 'sweep_le_deg':0, 'sweep_mt_deg':0,
                    'weightfractions': {'turn': 1.0, 'climb': 1.0, 'cruise': 1.0, 'servceil': 1.0},
                    'weight_n': co.kg2n(TOW_kg)}

designpropulsion = "piston"

designperformance = {'CDTO': 0.05, 'CLTO': 0.6, 'CLmaxTO': 1.6, 'CLmaxclean': 1.8, 'mu_R': 0.02,
                    'CDminclean': 0.04,
                    'etaprop': {'take-off': 0.6, 'climb': 0.6, 'cruise': 0.75, 'turn': 0.75, 'servceil': 0.75}}

concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm, designpropulsion)

wslist_pa = np.arange(300, 800, 2.5)

a = concept.propulsionsensitivity_monothetic(wingloading_pa=wslist_pa, show='combined', y_var='p_hp', x_var='s_m2', y_lim=150)