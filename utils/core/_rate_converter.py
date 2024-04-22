from utils.core import Rate, FrequencyType


class RateConverter:

    @staticmethod
    def convert_rate(rate: Rate, target_frequency: FrequencyType, method: str) -> Rate:
        if method == "SIMPLE":
            return RateConverter._convert_simple_rate(rate, target_frequency)
        elif method == "COMPOUND":
            return RateConverter._convert_compound_rate(rate, target_frequency)
        else:
            raise ValueError("Invalid method")

    @staticmethod
    def _convert_simple_rate(rate: Rate, target_frequency: FrequencyType) -> Rate:
        if rate.frequency == target_frequency:
            return rate
        rate_value = rate.value * rate.frequency.value / target_frequency.value
        return Rate(rate_value, target_frequency, rate.rate_type)

    @staticmethod
    def _convert_compound_rate(rate: Rate, target_frequency: FrequencyType) -> Rate:
        raise NotImplementedError("Compound rate conversion is not implemented yet")
