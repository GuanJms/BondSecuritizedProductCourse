from utils.core import FrequencyType, RateType
from decimal import Decimal

class Rate:
    def __init__(self, value: Decimal, frequency: FrequencyType, rate_type: RateType):
        self._type = rate_type
        self._value = value
        self._frequency = frequency

    @property
    def value(self):
        return self._value

    @property
    def frequency(self):
        return self._frequency

    @property
    def rate_type(self):
        return self._type

    def __copy__(self):
        return Rate(self.value, self.frequency, self.rate_type)

    def __eq__(self, other):
        return self.value == other.value and self.frequency == other.frequency and self.rate_type == other.rate_type

    def __ne__(self, other):
        return self.value != other.value or self.frequency != other.frequency or self.rate_type != other.rate_type

    def __str__(self):
        return f"{self.value}% {self.frequency} {self.rate_type}"

    def __repr__(self):
        return f"{self.value}% {self.frequency} {self.rate_type}"