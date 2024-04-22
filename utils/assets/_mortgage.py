from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from utils.assets import MortgageType
from utils.assets import Loan
from utils.core import *


class Mortgage(Loan):
    """
    Mortgage is a loan that is borrowed for purchasing House
    """

    def __init__(self, principal: Optional[Value] = None, rate: Optional[Rate] = None, maturity: Optional[Time] = None,
                 payment_frequency: Optional[FrequencyType] = None, mortgage_type: Optional['MortgageType'] = None):
        super().__init__(principal, rate, maturity)
        self._principal_payments: Optional[List[Value]] = None
        self._interest_payments: Optional[List[Value]] = None
        self._remaining_principals: Optional[List[Value]] = None
        self._payment_frequency = payment_frequency
        self._payment_periods: Optional[int] = None
        self._period_coupon_rate: Optional[Rate] = None
        self._mortgage_type = mortgage_type
        self._payment: Optional[Value] = None
        self._calculate_payment_periods()

        if self.rate is not None:
            self._period_coupon_rate = RateConverter.convert_rate(rate=self.rate,
                                                              target_frequency=self.payment_frequency,
                                                              method='SIMPLE')

    @property
    def period_coupon_rate(self) -> Rate:
        return self._period_coupon_rate

    @property
    def remaining_principals(self) -> List[Value]:
        return self._remaining_principals

    @property
    def interest_payments(self) -> List[Value]:
        return self._interest_payments

    @property
    def principal_payments(self) -> List[Value]:
        return self._principal_payments

    @property
    def mortgage_type(self) -> 'MortgageType':
        return self._mortgage_type

    @property
    def payment_frequency(self) -> FrequencyType:
        return self._payment_frequency

    @property
    def payment_periods(self) -> int:
        return self._payment_periods

    @property
    def payment(self) -> Optional[Value]:
        return self._payment

    def set_payment(self, payment):
        self._payment = payment

    def _calculate_payment_periods(self):
        if self.maturity is not None and self.payment_frequency is not None:
            self._payment_periods = int(self.maturity.value
                                        / FrequencyType.get_frequency_type(self.maturity.time_unit).value
                                        * self.payment_frequency.value)

    def set_lifecycle_payment_schedule(self, remaining_principals: List[Value], interest_payments: List[Value],
                                       principal_payments: List[Value]):
        self._remaining_principals = remaining_principals
        self._interest_payments = interest_payments
        self._principal_payments = principal_payments

    def set_weighted_average_life(self, weighted_average_life: Time):
        self._weighted_average_life = weighted_average_life

    def copy(self):
        principal = self.principal.__copy__()
        rate = self.rate.__copy__()
        maturity = self.maturity.__copy__()
        return Mortgage(principal=principal, rate=rate, maturity=maturity,
                        payment_frequency=self.payment_frequency, mortgage_type=self.mortgage_type)

    def set_maturity(self, maturity: Time):
        self._maturity = maturity
        self.reset()

    def reset(self):
        self._principal_payments = None
        self._interest_payments = None
        self._remaining_principals = None
        self._payment = None
        self._mortgage_type = None
        self._calculate_payment_periods()
