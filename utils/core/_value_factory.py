from decimal import Decimal
from typing import Optional

from utils.core import Value
from utils.core import CurrencyType


class ValueFactory:
    @staticmethod
    def create_value(value: str | float | Decimal, currency_type: Optional[CurrencyType] = None) -> Value:
        if isinstance(value, str):
            value = Decimal(value)
        elif isinstance(value, float):
            value = Decimal.from_float(value)
        elif isinstance(value, Decimal):
            pass  # value is already Decimal, no action needed
        else:
            raise ValueError("Invalid value type")

        if currency_type is None:
            currency_type = CurrencyType.USD

        return Value(value, currency_type)
