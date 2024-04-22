from decimal import Decimal

from utils.core import CurrencyType


class Value:
    def __init__(self, value: Decimal, currency: CurrencyType):
        self._value = value
        self._currency = currency

    @property
    def value(self):
        return self._value

    @property
    def currency(self) -> CurrencyType:
        return self._currency

    def __copy__(self):
        return Value(self.value, self.currency)

    def __add__(self, other):
        return Value(self.value + other.value, self.currency)

    def __sub__(self, other):
        return Value(self.value - other.value, self.currency)

    def __mul__(self, other):
        return Value(self.value * other, self.currency)

    def __truediv__(self, other):
        return Value(self.value / other, self.currency)

    def __eq__(self, other):
        return self.value == other.value and self.currency == other.currency

    def __ne__(self, other):
        return self.value != other.value or self.currency != other.currency

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __str__(self):
        return f"{self.currency.sign()}{round(self.value, 4)}"

    def __repr__(self):
        return f"{self.currency.sign()}{round(self.value, 4)}"
