# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 11:30:44 2015

@author: thomas.douenne
"""

import datetime
import pandas as pd

from openfisca_france_indirect_taxation.tests import base
from openfisca_france_indirect_taxation.example.utils_example import graph_builder_line

index = range(2002, 2014)
columns = ['si une essence et une diesel', 'si seulement vehicules diesel', 'si seulement vehicules essence']
depenses_ticpe_pour_100_euros_carbu = pd.DataFrame(index = index, columns = columns)

for element in columns:
    if element == 'si seulement vehicules essence':
        dies = 0
    else:
        dies = 1
    if element == 'si seulement vehicules diesel':
        ess = 0
    else:
        ess = 1
    for year in range(2002, 2014):
        year = year
        simulation = base.tax_benefit_system.new_scenario().init_single_entity(
            period = year,
            personne_de_reference = dict(
                birth = datetime.date(year - 40, 1, 1),
                ),
            menage = dict(
                consommation_ticpe = 500,
                veh_essence = ess,
                veh_diesel = dies,
                ),
            ).new_simulation(debug = True)

        depenses_ticpe_pour_100_euros_carbu.loc[depenses_ticpe_pour_100_euros_carbu.index == year, element] = \
            simulation.calculate('ticpe_totale')

graph_builder_line(depenses_ticpe_pour_100_euros_carbu)