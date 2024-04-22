from typing import Optional

from utils.assets import Mortgage, MortgagePool
from utils.core import Rate, Time, FrequencyType, Value, CurrencyType, RateType
from utils.core import ValueFactory, RateFactory
from utils.assets._enums import MortgageType
from decimal import Decimal


class MortgagePoolFactory:

    @staticmethod
    def create_same_mortgage_type_pool(**kwargs):
        mortgage_pool = MortgagePool(**kwargs)
        return mortgage_pool




