import pandas as pd
import re

from fdms.config.variable_groups import PD
from fdms.config.country_groups import FCRIF
from fdms.utils.mixins import StepMixin
from fdms.utils.series import get_series, get_series_noindex, export_to_excel, get_scale
from fdms.utils.operators import Operators


class LabourMarket(StepMixin):
    def perform_computation(self, df):
        if self.country in FCRIF:
            pass
