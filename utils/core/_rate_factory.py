from decimal import Decimal

from utils.core import Rate, FrequencyType, RateType


class RateFactory:
    @staticmethod
    def create_rate(value: str | float | Decimal, frequency: FrequencyType, rate_type: RateType) -> Rate:
        if isinstance(value, str):
            value = Decimal(value)
        elif isinstance(value, float):
            value = Decimal.from_float(value)
        elif isinstance(value, Decimal):
            pass
        return Rate(value, frequency, rate_type)
