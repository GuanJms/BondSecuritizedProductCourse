from typing import Union

from utils.core import TimeUnit
import warnings


class Time:
    def __init__(self, value: float, time_unit: TimeUnit):
        self._value = value
        self._time_unit = time_unit

    @property
    def value(self):
        return self._value

    @property
    def time_unit(self):
        return self._time_unit

    def __copy__(self):
        return Time(self.value, self.time_unit)

    def convert_to(self, time_unit: TimeUnit):
        if time_unit == self.time_unit:
            return self
        match time_unit:
            case TimeUnit.SECOND:
                return Time(self.value * self.time_unit.value, TimeUnit.SECOND)
            case TimeUnit.MINUTE:
                return Time(self.value * self.time_unit.value / TimeUnit.MINUTE.value, TimeUnit.MINUTE)
            case TimeUnit.HOUR:
                return Time(self.value * self.time_unit.value / TimeUnit.HOUR.value, TimeUnit.HOUR)
            case TimeUnit.DAY:
                return Time(self.value * self.time_unit.value / TimeUnit.DAY.value, TimeUnit.DAY)
            case TimeUnit.WEEK:
                return Time(self.value * self.time_unit.value / TimeUnit.WEEK.value, TimeUnit.WEEK)
            case TimeUnit.MONTH:
                return Time(self.value * self.time_unit.value / TimeUnit.MONTH.value, TimeUnit.MONTH)
            case TimeUnit.QUARTER:
                return Time(self.value * self.time_unit.value / TimeUnit.QUARTER.value, TimeUnit.QUARTER)
            case TimeUnit.SEMI_YEAR:
                return Time(self.value * self.time_unit.value / TimeUnit.SEMI_YEAR.value, TimeUnit.SEMI_YEAR)
            case TimeUnit.YEAR:
                return Time(self.value * self.time_unit.value / TimeUnit.YEAR.value, TimeUnit.YEAR)
            case TimeUnit.TWO_YEAR:
                return Time(self.value * self.time_unit.value / TimeUnit.TWO_YEAR.value, TimeUnit.TWO_YEAR)
            case _:
                raise ValueError("Invalid time unit")

    def is_time_class(self, other: 'Time'):
        if not isinstance(other, Time):
            raise TypeError(f"unsupported operand type(s) for /: 'Time' and '{type(other)}'")

    def __abs__(self):
        return Time(abs(self.value), self.time_unit)

    def __round__(self, n: int):
        return Time(round(self.seconds.value, n), TimeUnit.SECOND)

    def __truediv__(self, divisor: Union['Time', int, float]):
        if isinstance(divisor, (int, float)):
            if divisor == 0:
                raise ZeroDivisionError("division by zero")
            return Time(self.value / divisor, self.time_unit)
        self.is_time_class(divisor)
        if divisor.value == 0:
            raise ZeroDivisionError("division by zero")
        return (self.value / divisor.value) * (self.time_unit.value / divisor.time_unit.value)

    def __floordiv__(self, divisor: 'Time'):
        self.is_time_class(divisor)
        if divisor.value == 0:
            raise ZeroDivisionError("division by zero")
        # raise warning that this is not accurate
        warnings.warn("__floordiv__ might contain numerical error")
        if self.time_unit == divisor.time_unit:
            return self.value // divisor.value
        return self.seconds // divisor.seconds

    def __mul__(self, other: float):
        if not isinstance(other, (int, float)):
            raise TypeError(f"unsupported operand type(s) for *: 'Time' and '{type(other)}'")
        return Time(self.value * other, self.time_unit)

    def __add__(self, other: 'Time'):
        self.is_time_class(other)
        return Time(self.seconds.value + other.seconds.value, TimeUnit.SECOND)

    def __sub__(self, other: 'Time'):
        self.is_time_class(other)
        return Time(self.seconds.value - other.seconds.value, TimeUnit.SECOND)

    def __eq__(self, other: 'Time'):
        self.is_time_class(other)
        if self.time_unit == other.time_unit:
            return self.value == other.value
        return self.seconds.value == other.seconds.value

    def __ne__(self, other: 'Time'):
        self.is_time_class(other)
        if self.time_unit == other.time_unit:
            return self.value != other.value
        return self.seconds.value != other.seconds.value

    def __lt__(self, other: 'Time'):
        self.is_time_class(other)
        if self.time_unit == other.time_unit:
            return self.value < other.value
        return self.seconds.value < other.seconds.value

    def __le__(self, other: 'Time'):
        self.is_time_class(other)
        if self.time_unit == other.time_unit:
            return self.value <= other.value
        return self.seconds.value <= other.seconds.value

    def __gt__(self, other: 'Time'):
        self.is_time_class(other)
        if self.time_unit == other.time_unit:
            return self.value > other.value
        return self.seconds.value > other.seconds.value

    def __ge__(self, other: 'Time'):
        self.is_time_class(other)
        if self.time_unit == other.time_unit:
            return self.value >= other.value
        return self.seconds.value >= other.seconds.value

    def __str__(self):
        print(self.value, self.time_unit.printable_unit())
        return f"{round(self.value, 2)} {self.time_unit.printable_unit()}"

    def __repr__(self):
        return f"{round(self.value, 2)} {self.time_unit.printable_unit()}"
