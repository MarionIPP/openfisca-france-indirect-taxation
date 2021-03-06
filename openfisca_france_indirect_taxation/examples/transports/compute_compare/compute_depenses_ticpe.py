# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 17:52:53 2015

@author: thomas.douenne
"""


# Import de modules généraux
from __future__ import division

import csv
import pkg_resources
import os

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import simulate_df_calee_on_ticpe


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    simulated_variables_with_e10 = [
        'pondmen',
        'sp_e10_ticpe',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe'
        ]

    simulated_variables_without_e10 = [
        'pondmen',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe'
        ]

    # Calcul des contributions agrégées des ménages sur la TICPE, dont diesel et essence
    depenses_ticpe_totales = dict()
    depenses_ticpe_diesel = dict()
    depenses_ticpe_essence = dict()
    for year in [2000, 2005, 2011]:
        try:
            data_simulation = \
                simulate_df_calee_on_ticpe(simulated_variables = simulated_variables_with_e10, year = year)
            depenses_diesel_ticpe = (data_simulation['diesel_ticpe'] * data_simulation['pondmen']).sum()
            depenses_sp95_ticpe = (data_simulation['sp95_ticpe'] * data_simulation['pondmen']).sum()
            depenses_sp98_ticpe = (data_simulation['sp98_ticpe'] * data_simulation['pondmen']).sum()
            depenses_super_plombe_ticpe = (data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']).sum()
            depenses_sp_e10_ticpe = (data_simulation['sp_e10_ticpe'] * data_simulation['pondmen']).sum()
        except:
            data_simulation = \
                simulate_df_calee_on_ticpe(simulated_variables = simulated_variables_without_e10, year = year)
            depenses_diesel_ticpe = (data_simulation['diesel_ticpe'] * data_simulation['pondmen']).sum()
            depenses_sp95_ticpe = (data_simulation['sp95_ticpe'] * data_simulation['pondmen']).sum()
            depenses_sp98_ticpe = (data_simulation['sp98_ticpe'] * data_simulation['pondmen']).sum()
            depenses_super_plombe_ticpe = (data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']).sum()
            depenses_sp_e10_ticpe = 0

        if year < 2007:
            depenses_essence_ticpe = (
                depenses_sp95_ticpe +
                depenses_sp98_ticpe +
                depenses_sp_e10_ticpe +
                depenses_super_plombe_ticpe
                )
        else:
            depenses_essence_ticpe = (
                depenses_sp95_ticpe +
                depenses_sp98_ticpe +
                depenses_sp_e10_ticpe
                )

        depenses_ticpe = depenses_diesel_ticpe + depenses_essence_ticpe
        depenses_ticpe_totales['en millions d euros en {}'.format(year)] = depenses_ticpe / 1000000
        depenses_ticpe_diesel['en millions d euros en {}'.format(year)] = depenses_diesel_ticpe / 1000000
        depenses_ticpe_essence['en millions d euros en {}'.format(year)] = depenses_essence_ticpe / 1000000

    # Enregistrement des montants agrégées dans des fichiers csv
    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )

    writer_carburants = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'depenses', 'depenses_ticpe_totales_bdf.csv'), 'wb'))
    for key, value in depenses_ticpe_totales.items():
        writer_carburants.writerow([key, value])

    writer_diesel = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'depenses', 'depenses_ticpe_diesel_bdf.csv'), 'wb'))
    for key, value in depenses_ticpe_diesel.items():
        writer_diesel.writerow([key, value])

    writer_essence = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'depenses', 'depenses_ticpe_essence_bdf.csv'), 'wb'))
    for key, value in depenses_ticpe_essence.items():
        writer_essence.writerow([key, value])
