from typing import Optional

from utils.assets import Mortgage
from utils.core import Rate, Time, FrequencyType, Value, CurrencyType, RateType
from utils.core import ValueFactory, RateFactory
from utils.assets._enums import MortgageType


class MortgageFactory:

    @staticmethod
    def create_mortgage(principal: str | float| Value | None = None, rate: Rate | None = None, maturity: Time | None = None,
                        payment_frequency: FrequencyType | None = None , mortgage_type: MortgageType | None = None,
                        currency_type: Optional[CurrencyType] = None) -> Mortgage:
        match mortgage_type:
            case MortgageType.FIXED_RATE:
                if isinstance(principal, (str, float)):
                    principal = ValueFactory.create_value(value=principal, currency_type=currency_type)
                if rate is not None and rate.rate_type != RateType.FIXED:
                    raise ValueError("Fixed rate mortgage should have fixed rate type")
                return Mortgage(principal=principal, rate=rate, maturity=maturity,
                                payment_frequency=payment_frequency, mortgage_type=mortgage_type)
            case _:
                raise ValueError(f"MortgageType: {mortgage_type} not supported")
