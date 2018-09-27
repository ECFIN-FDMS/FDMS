import pandas as pd

from fdms.utils.series import COLUMN_ORDER


class StepMixin:
    result = pd.DataFrame(columns=COLUMN_ORDER)
    country = 'BE'
    frequency = 'Annual'
    scale = 'units'

    def __init__(self, country=country, frequency=frequency, scale=scale):
        self.country = country
        self.frequency = frequency
        self.scale = scale
