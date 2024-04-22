from utils.assets import Mortgage
from utils.calculator import MortgageCalculator
from utils.core import FrequencyType, TimeUnit, Time
from utils.core import RateConverter


class FixedCouponRateMortgageCalculator(MortgageCalculator):
    """
    Mortgage calculator with fixed coupon rate type mortgage without prepayment
    """

    @staticmethod
    def calculate_payment(mortgage: Mortgage):
        match mortgage.payment_frequency:
            case FrequencyType.MONTHLY:
                # Calculate monthly payment
                c = mortgage.period_coupon_rate.value
                M0 = mortgage.principal
                _n = mortgage.payment_periods
                _compound_rate = (1 + c) ** _n
                _B = M0 * c * _compound_rate / (_compound_rate - 1)  # _B: monthly payment
                mortgage.set_payment(payment=_B)
            case _:
                raise ValueError(f"Mortgage FrequencyType: {mortgage.payment_frequency} not supported ")

    @staticmethod
    def calculate_interest_payment(mortgage: Mortgage, period: int):
        raise NotImplementedError

    @staticmethod
    def calculate_principal_payment(mortgage: Mortgage, period: int):
        raise NotImplementedError

    @staticmethod
    def calculate_remaining_principal(mortgage: Mortgage, period: int):
        raise NotImplementedError

    @staticmethod
    def calculate_lifecycle_payment_schedule(mortgage: Mortgage):
        if mortgage.payment is None:
            FixedCouponRateMortgageCalculator.calculate_payment(mortgage)
        c = mortgage.period_coupon_rate.value
        M0 = mortgage.principal
        # Calculate lifecycle payment schedule
        remaining_principals = [M0]
        interest_payments = []
        principal_payments = []
        for i in range(mortgage.payment_periods):
            interest_payment = remaining_principals[i] * c
            principal_payment = mortgage.payment - interest_payment
            remaining_principal = remaining_principals[i] - principal_payment
            remaining_principals.append(remaining_principal)
            interest_payments.append(interest_payment)
            principal_payments.append(principal_payment)
        remaining_principals.pop(0)
        mortgage.set_lifecycle_payment_schedule(remaining_principals=remaining_principals,
                                                interest_payments=interest_payments,
                                                principal_payments=principal_payments)

    @staticmethod
    def calculate_weighted_average_life(mortgage: Mortgage, current_period: int) -> Time:
        if mortgage.principal_payments is None:
            FixedCouponRateMortgageCalculator.calculate_lifecycle_payment_schedule(mortgage)
        n = mortgage.payment_periods
        time_unit = mortgage.payment_frequency.get_time_unit()
        k = current_period  # Current time point
        principal_payments = [0] + [x.value for x in mortgage.principal_payments]
        times = [i for i in range(0, n + 1)]
        if current_period >= n:
            return Time(0, time_unit)
        weighted_average_life_value = sum(
            [(times[i] - k) * principal_payments[i] for i in range(current_period + 1, n+1)]) / sum(
            principal_payments[current_period + 1:])
        weighted_average_life = Time(weighted_average_life_value, time_unit)
        return weighted_average_life
