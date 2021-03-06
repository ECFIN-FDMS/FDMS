import pandas as pd
import re

from fdms.computation.country.annual.transfer_matrix import TransferMatrix
from fdms.computation.country.annual.population import Population
from fdms.computation.country.annual.national_accounts_components import GDPComponents
from fdms.computation.country.annual.national_accounts_volume import NationalAccountsVolume
from fdms.config import FORECAST, AMECO, AMECO_SHEET
from fdms.utils.interfaces import read_country_forecast_excel, read_ameco_txt


class Compute:
    def __init__(self, country_forecast_filename=FORECAST, ameco_filename=AMECO, ameco_sheet_name=AMECO_SHEET):
        self.excel_raw = country_forecast_filename
        self.ameco_filename = ameco_filename
        self.ameco_sheet_name = ameco_sheet_name

    def perform_computation(self):
        df, ameco_df = read_country_forecast_excel(), read_ameco_txt()

        ##################################################################
        # If Country in group 'Forecast: Countries from transfer matrix' #
        ##################################################################

        # Convert all transfer matrix variables to 1.0.0.0 (except National Account (volume)) and splice in country
        # desk forecast
        ###########################################################################################################

        step_1 = TransferMatrix()
        result_1 = step_1.perform_computation(df, ameco_df)
        self.result = result_1.copy()

        # Population and related variables - splice AMECO Historical data with forecast data
        ####################################################################################

        step_2_vars = ['NUTN.1.0.0.0', 'NETN.1.0.0.0', 'NWTD.1.0.0.0', 'NETD.1.0.0.0', 'NPAN1.1.0.0.0', 'NETN',
                       'NLHA.1.0.0.0']
        # NECN.1.0.0.0 is calculated and used in step_2
        step_2_df = result_1.loc[result_1.index.isin(step_2_vars, level='Variable Code')].copy()
        step_2 = Population()
        result_2 = step_2.perform_computation(step_2_df, ameco_df)
        self.result = pd.concat([self.result, result_2], sort=True)

        # National Accounts - Calculate additional GDP components
        # National Accounts (Value) - calculate additional components
        ####################################################################################

        step_3_vars = ['UMGN', 'UMSN', 'UXGN', 'UXSN', 'UMGN', 'UMSN', 'UXGS', 'UMGS', 'UIGG0', 'UIGT', 'UIGG', 'UIGCO',
                       'UIGDW', 'UCPH', 'UCTG', 'UIGT', 'UIST']
        step_3_additional_vars = ['UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UMGN.1.0.0.0',
                                  'UMSN.1.0.0.0', 'UXGS.1.0.0.0', 'UMGS.1.0.0.0', 'UIGG0.1.0.0.0', 'UIGT.1.0.0.0',
                                  'UIGG.1.0.0.0', 'UIGCO.1.0.0.0', 'UIGDW.1.0.0.0', 'UCPH.1.0.0.0', 'UCTG.1.0.0.0',
                                  'UIGT.1.0.0.0', 'UIST.1.0.0.0', 'UXGN', 'UMGN']
        step3_vars = set(step_3_vars + step_3_additional_vars)
        step_3_df = result_1.loc[result_1.index.isin(step_3_vars, level='Variable Code')].copy()
        ameco_series = ameco_df.loc[ameco_df.index.isin(step_3_additional_vars, level='Variable Code')].copy()
        step_3_df = step_3_df.append(ameco_series)
        step_3 = GDPComponents()
        # result_3 = step_3.perform_computation(step_3_df)
        # self.result = pd.concat([self.result, result_3], sort=True)

        # National Accounts (Volume) - splice AMECO Historical data with forecast data, calculate year/year percent
        #  change, per-capita GDP, and contribution to %change in GDP
        ####################################################################################

        step_4_vars = ['UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UMGN.1.0.0.0', 'UMSN.1.0.0.0',
                       'UXGS.1.0.0.0', 'UMGS.1.0.0.0', 'UIGG0.1.0.0.0', 'UIGT.1.0.0.0', 'UIGG.1.0.0.0', 'UIGCO.1.0.0.0',
                       'UIGDW.1.0.0.0', 'UCPH.1.0.0.0', 'UCTG.1.0.0.0', 'UIGT.1.0.0.0', 'UIST.1.0.0.0', 'UXGN', 'UMGN']
        step_4_df = result_1.loc[result_1.index.isin(step_4_vars, level='Variable Code')].copy()
        step_4 = NationalAccountsVolume()
        # result_4 = step_4.perform_computation(step_4_df)
        # self.result = pd.concat([self.result, result_4], sort=True)
