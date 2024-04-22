import unittest
from utils.assets import MortgageFactory
from utils.core import *
from utils.assets import *
from utils.calculator.mortgage.no_prepayment import FixedCouponRateMortgageCalculator


class MyTestCase(unittest.TestCase):
    def setUp(self):
        value_str = '100000'
        rate_str = '0.04'
        initial_principal = ValueFactory.create_value(value_str, currency_type=CurrencyType.USD)
        annual_coupon = RateFactory.create_rate(value=rate_str, rate_type=RateType.FIXED,
                                                frequency=FrequencyType.ANNUALLY)
        self.mortgage = MortgageFactory.create_mortgage(principal=initial_principal,
                                                        rate=annual_coupon,
                                                        maturity=Time(180, TimeUnit.MONTH),
                                                        payment_frequency=FrequencyType.MONTHLY,
                                                        mortgage_type=MortgageType.FIXED_RATE)

    def test_fixed_coupon_rate_mortgage_calculator(self):
        FixedCouponRateMortgageCalculator.calculate_payment(self.mortgage)
        print("Payment: ", self.mortgage.payment)
        FixedCouponRateMortgageCalculator.calculate_lifecycle_payment_schedule(self.mortgage)
        print("Principal Payments: ", self.mortgage.principal_payments[:5])
        print("Interest Payments: ", self.mortgage.interest_payments[:5])
        print("Remaining Principals: ", self.mortgage.remaining_principals[:5])
        self.assertAlmostEqual(
            sum([principal_payment.value for principal_payment in self.mortgage.principal_payments]),
            self.mortgage.principal.value, places=2)
        print(self.mortgage.remaining_principals[-1].value)

    def test_WAL_calculation(self):
        FixedCouponRateMortgageCalculator.calculate_weighted_average_life(self.mortgage, 0)



if __name__ == '__main__':
    unittest.main()
