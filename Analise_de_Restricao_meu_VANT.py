# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:58:47 2022

@author: JOÃO GABRIEL DAL FORNO - DADOS DO MEU VANT
"""

import numpy as np
import matplotlib.pyplot as plt
from ADRpy import unitconversions as co
from ADRpy import constraintanalysis as ca
from ADRpy import atmospheres as at

designbrief = {# Requisitos de Decolagem:
               'rwyelevation_m':0, 'groundrun_m':60, 
               # Requisitos de Curva
               'stloadfactor': 1.41, 'turnalt_m': 0, 'turnspeed_ktas': 40,
               # Requisitos de Subida
               'climbalt_m': 0, 'climbspeed_kias': 46.4, 'climbrate_fpm': 591,
               # Requisitos de Cruzeiro
               'cruisealt_m': 122, 'cruisespeed_ktas': 30.615, 'cruisethrustfact': 1.0, 
               # Teto de Voo
               'servceil_m': 984, 'secclimbspd_kias': 40, 
               # Velocidade de Estol requerida
               'vstallclean_kcas': 17.70} 

wfract = {'turn': 1.0, 'climb': 1.0, 'cruise': 1.0, 'servceil': 1.0}

designdefinition = {'aspectratio':7.5, 'sweep_le_deg':2, 'sweep_mt_deg':0, 'weightfractions':wfract} 

etap = {'take-off': 0.6, 'climb': 0.6, 'cruise': 0.6, 'turn': 0.6, 'servceil': 0.6}

designperformance = {'CDTO':0.0898, 'CLTO':0.97, 'CLmaxTO':1.7, 'CLmaxclean': 1.0, 'mu_R':0.17, 
                     'CDminclean':0.0418, 'etaprop': etap}

TOW_kg = 3.4

designatm = at.Atmosphere()

concept = ca.AircraftConcept(designbrief, designdefinition, designperformance, designatm, "piston")

wingloadinglist_pa = np.arange(25, 2500, 2.5)

preq = concept.powerrequired(wingloadinglist_pa, TOW_kg) 

Smin_m2 = concept.smincleanstall_m2(TOW_kg)

#%matplotlib notebook

wingarea_m2 = co.kg2n(TOW_kg) / wingloadinglist_pa # x axis

plt.rcParams["figure.figsize"] = [8,6]
plt.plot(wingarea_m2, preq['take-off'], label = 'Take-off')
plt.plot(wingarea_m2, preq['turn'], label = 'Turn')
plt.plot(wingarea_m2, preq['climb'], label = 'Climb')
plt.plot(wingarea_m2, preq['cruise'], label = 'Cruise')
plt.plot(wingarea_m2, preq['servceil'], label = 'Service ceiling')
combplot = plt.plot(wingarea_m2, preq['combined'], label = 'Combined')
plt.setp(combplot, linewidth=4)
stall_label = 'Clean stall at ' + str(designbrief['vstallclean_kcas']) + 'KCAS'
plt.plot([Smin_m2, Smin_m2], [0, 1500], label = stall_label)
legend = plt.legend(loc='upper left')
plt.ylabel("Power required (HP)")
plt.xlabel("S (m$^2$)")
plt.title("Minimum SL power required (MTOW = " + str(round(TOW_kg)) + "kg)")
plt.xlim(0, 3)
plt.ylim(0, 5)
plt.grid(True)
plt.text(1.5, 4, 'Feasible region')
plt.show()

#T/W versus wing loading

twreq = concept.twrequired(wingloadinglist_pa)

clmaxapproach = 1.3
WSmax_clean_stall = concept.wsmaxcleanstall_pa()
WSmax_approach_stall = WSmax_clean_stall / concept.clmaxclean * clmaxapproach
print(WSmax_approach_stall)


plt.rcParams["figure.figsize"] = [8,6]
plt.plot(wingloadinglist_pa, twreq['take-off'], label = 'Take-off')
plt.plot(wingloadinglist_pa, twreq['turn'], label = 'Turn')
plt.plot(wingloadinglist_pa, twreq['climb'], label = 'Climb')
plt.plot(wingloadinglist_pa, twreq['cruise'], label = 'Cruise')
plt.plot(wingloadinglist_pa, twreq['servceil'], label = 'Service ceiling')
combplot = plt.plot(wingloadinglist_pa, twreq['combined'], label = 'Combined')

plt.plot([WSmax_approach_stall, WSmax_approach_stall], [0, 0.6], label = stall_label)

legend = plt.legend(loc='upper left')
plt.ylabel("T/W required ()")
plt.xlabel("W/S (Pa)")
plt.title("Minimum sea level T/W required")
plt.xlim(0, 200)
plt.ylim(0, 0.6)
plt.grid(True)
plt.text(100, 0.5, 'Feasible region')
plt.show()

plt.show()

# Power versus wing loading

wingloadinglist_kgm2 = co.pa2kgm2(wingloadinglist_pa)

plt.rcParams["figure.figsize"] = [8,6]
plt.plot(wingloadinglist_kgm2, co.hp2kw(preq['take-off']), label = 'Take-off')
plt.plot(wingloadinglist_kgm2, co.hp2kw(preq['turn']), label = 'Turn')
plt.plot(wingloadinglist_kgm2, co.hp2kw(preq['climb']), label = 'Climb')
plt.plot(wingloadinglist_kgm2, co.hp2kw(preq['cruise']), label = 'Cruise')
plt.plot(wingloadinglist_kgm2, co.hp2kw(preq['servceil']), label = 'Service ceiling')
combplot = plt.plot(wingloadinglist_kgm2, co.hp2kw(preq['combined']), label = 'Combined')

plt.setp(combplot, linewidth=4)


plt.plot([co.pa2kgm2(WSmax_approach_stall),
          co.pa2kgm2(WSmax_approach_stall)], [0, 5], label = stall_label)


legend = plt.legend(loc='upper left')
plt.ylabel("Power required (kW)")
plt.xlabel("W/S (kg/m$^2$)")
plt.title("Minimum SL power required (MTOW = " + str(round(TOW_kg)) + "kg)")
plt.xlim(0, 20)
plt.ylim(0, 4)
plt.grid(True)

plt.show()






