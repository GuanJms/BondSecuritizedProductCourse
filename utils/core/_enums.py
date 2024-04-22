from enum import Enum, auto


class CurrencyType(Enum):
    USD = auto()
    EURO = auto()
    POUND = auto()
    YEN = auto()
    YUAN = auto()

    def sign(self):
        if self == CurrencyType.USD:
            return '$'
        elif self == CurrencyType.EURO:
            return '€'
        elif self == CurrencyType.POUND:
            return '£'
        elif self == CurrencyType.YEN:
            return '¥'
        elif self == CurrencyType.YUAN:
            return '¥'


class TimeUnit(Enum):
    MILLISECOND = 1 / 1000
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2628000
    QUARTER = 7884000
    SEMI_YEAR = 15768000
    YEAR = 31536000
    TWO_YEAR = 63072000

    def printable_unit(self):
        if self == TimeUnit.MILLISECOND:
            return 'ms'
        elif self == TimeUnit.SECOND:
            return 's'
        elif self == TimeUnit.MINUTE:
            return 'min'
        elif self == TimeUnit.HOUR:
            return 'hr'
        elif self == TimeUnit.DAY:
            return 'day'
        elif self == TimeUnit.WEEK:
            return 'wk'
        elif self == TimeUnit.MONTH:
            return 'mo'
        elif self == TimeUnit.QUARTER:
            return 'qtr'
        elif self == TimeUnit.SEMI_YEAR:
            return 'semi-yr'
        elif self == TimeUnit.YEAR:
            return 'yr'
        elif self == TimeUnit.TWO_YEAR:
            return '2-yr'


class FrequencyType(Enum):
    DAILY = 365
    WEEKLY = 52
    MONTHLY = 12
    QUARTERLY = 4
    SEMI_ANNUALLY = 2
    ANNUALLY = 1
    BI_ANNUALLY = 1 / 2

    def get_time_unit(self) -> 'TimeUnit':
        if self == FrequencyType.DAILY:
            return TimeUnit.DAY
        elif self == FrequencyType.WEEKLY:
            return TimeUnit.WEEK
        elif self == FrequencyType.MONTHLY:
            return TimeUnit.MONTH
        elif self == FrequencyType.QUARTERLY:
            return TimeUnit.QUARTER
        elif self == FrequencyType.SEMI_ANNUALLY:
            return TimeUnit.SEMI_YEAR
        elif self == FrequencyType.ANNUALLY:
            return TimeUnit.YEAR
        elif self == FrequencyType.BI_ANNUALLY:
            return TimeUnit.TWO_YEAR

    @staticmethod
    def get_frequency_type(time_unit: 'TimeUnit') -> 'FrequencyType':
        if time_unit == TimeUnit.DAY:
            return FrequencyType.DAILY
        elif time_unit == TimeUnit.WEEK:
            return FrequencyType.WEEKLY
        elif time_unit == TimeUnit.MONTH:
            return FrequencyType.MONTHLY
        elif time_unit == TimeUnit.QUARTER:
            return FrequencyType.QUARTERLY
        elif time_unit == TimeUnit.SEMI_YEAR:
            return FrequencyType.SEMI_ANNUALLY
        elif time_unit == TimeUnit.YEAR:
            return FrequencyType.ANNUALLY
        elif time_unit == TimeUnit.TWO_YEAR:
            return FrequencyType.BI_ANNUALLY


class RateType(Enum):
    FIXED = auto()
    FLOATING = auto()
