import unittest
from utils.core import *
from utils.assets import *

class MyTestMortgage(unittest.TestCase):
    def setUp(self):
        initial_principal = ValueFactory.create_value('100000', currency_type= CurrencyType.USD)
        annual_coupon = RateFactory.create_rate(value='0.04', rate_type=RateType.FIXED, frequency=FrequencyType.ANNUALLY)
        self.mortgage = MortgageFactory.create_mortgage(principal=initial_principal,
                                                        rate=annual_coupon,
                                                        maturity=Time(30, TimeUnit.YEAR),
                                                        payment_frequency=FrequencyType.MONTHLY,
                                                        mortgage_type=MortgageType.FIXED_RATE)

    def test_mortgage(self):
        self.assertEqual(self.mortgage.principal, ValueFactory.create_value('100000', currency_type= CurrencyType.USD))
        self.assertEqual(self.mortgage.rate, RateFactory.create_rate(value='0.04', rate_type=RateType.FIXED, frequency=FrequencyType.ANNUALLY))
        self.assertEqual(self.mortgage.maturity, Time(30, TimeUnit.YEAR))
        self.assertEqual(self.mortgage.payment_frequency, FrequencyType.MONTHLY)
        self.assertEqual(self.mortgage.mortgage_type, MortgageType.FIXED_RATE)
        self.assertEqual(self.mortgage.payment, None)



if __name__ == '__main__':
    unittest.main()
