from typing import List
from utils.assets import Mortgage
from utils.core import Rate, Time, Value, ValueFactory, FrequencyType
from decimal import Decimal


class MortgagePool:
    def __init__(self, **kwargs):
        self._payment_periods: int = None
        self._mortgages: List[Mortgage] | None = kwargs.get('mortgages', None)
        self._loan_number: int | None = kwargs.get('loan_number', None)
        self._pool_type = kwargs.get('pool_type', None)
        self._loan_size: Value | None = kwargs.get('loan_size', None)
        self._WAC: Rate | None = kwargs.get('WAC', None)
        self._WALA: Time | None = kwargs.get('WALA', None)
        self._SMM: Rate | None = kwargs.get('SMM', None)
        self._maturity: Time | None = kwargs.get('maturity', None)
        self._payment_frequency: Time | None = kwargs.get('payment_frequency', None)
        self._total_fee: Decimal | None = kwargs.get('total_fee', None)

    def get_param(self, param):
        if hasattr(self, param):
            return getattr(self, param)
        if hasattr(self, f'_{param}'):
            return getattr(self, f'_{param}')
        return None

    def get_payment_periods(self) -> int:
        if self._payment_periods is None:
            if self._maturity is not None and self._payment_frequency is not None:
                self._payment_periods = int(self._maturity.value
                                            / FrequencyType.get_frequency_type(self._maturity.time_unit).value
                                            * self._payment_frequency.value)
        return self._payment_periods


