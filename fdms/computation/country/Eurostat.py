
import pandas as pd
from fdms.config.variable_groups import HICP
import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class EurostatInput:

    def read_eurostat_data_excel(self, filename,sheet):
        # converts the input to a pandas dataframe
        dataframe = pd.read_excel(filename, sheet_name=sheet, header=0)
        return dataframe

    def filtering_taging_group(self, dataframe,group='HICP',tag='1.0.0.0'):
        # filters the records in the group specified and adds a tag

        dataframe.loc[dataframe['Variable'].isin(group)]
        dataframe['Code'] = dataframe['Series'].str.split('.', 1).str[0]
        dataframe['Series'] = dataframe['Code'] + '.' + tag + '.' + dataframe['Variable'] + '.'
        dataframe['Variable'] = dataframe['Variable'] + '.' + tag
        dataframe.drop(columns=['Code'], inplace=True)
        return dataframe


    def dataframe_sampler(self, dataframe,period):
        if period == 'M':
            monthly_df = dataframe
            monthly_df['Series'] = monthly_df['Series'] + 'M'
            monthly_df = dataframe.set_index(['Series'])
            return monthly_df
        else: # preparation of the dataframe before resampling from 'M' to ('Q' or 'A')
            dataframe = dataframe.set_index(['Series', 'Country', 'Variable', 'Scale', 'F'])
            dataframe.columns = [x.strip().replace('M', '-') for x in dataframe.columns]
            dataframe.columns = pd.to_datetime(dataframe.columns, errors='ignore')
            dataframe.to_period(freq='M', axis=1)
            if period == 'Q':
                quarter_df = dataframe.resample('Q-DEC', axis=1).mean().to_period(freq='Q', axis=1)
                quarter_df.columns = quarter_df.columns.map(str)
                quarter_df = quarter_df.reset_index()
                quarter_df['F'] = 'Q'
                quarter_df['Series'] = quarter_df['Series'] + 'Q'
                quarter_df = quarter_df.set_index('Series')
                return quarter_df
            if period == 'A':
                annual_df = dataframe.resample('A-DEC', axis=1).mean().to_period(freq='A', axis=1)
                annual_df.columns = annual_df.columns.map(str)
                annual_df = annual_df.reset_index()
                annual_df['F'] = 'A'
                annual_df['Series'] = annual_df['Series'] + 'A'
                annual_df = annual_df.set_index('Series')
                return annual_df

    def hicp_quarterly(self,filename,sheet):
        group = HICP
        tag = '1.0.0.0'
        dataframe = self.read_eurostat_data_excel(filename,sheet)
        dataframe = self.filtering_taging_group(dataframe,group,tag)
        eurostat_quarter = self.dataframe_sampler(dataframe,'Q')
        return eurostat_quarter

    def set_EU_EA_numbers(self):
        pass

    def start_end_update_date(self):
        pass
