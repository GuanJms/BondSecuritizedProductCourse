import unittest
from utils.core import TimeUnit, Time



class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.millisecond = Time(1, TimeUnit.MILLISECOND)
        self.second = Time(1, TimeUnit.SECOND)
        self.minute = Time(1, TimeUnit.MINUTE)
        self.hour = Time(1, TimeUnit.HOUR)
        self.day = Time(1, TimeUnit.DAY)
        self.week = Time(1, TimeUnit.WEEK)
        self.month = Time(1, TimeUnit.MONTH)
        self.year = Time(1, TimeUnit.YEAR)

        # Multiplication tests

    def test_multiplication(self):
        self.assertEqual(self.hour * 24, Time(1, TimeUnit.DAY))
        self.assertEqual(self.minute * 60, Time(1, TimeUnit.HOUR))
        self.assertEqual(self.second * 60, Time(1, TimeUnit.MINUTE))
        self.assertEqual(self.day * 7, Time(1, TimeUnit.WEEK))
        self.assertAlmostEquals(self.month * 12, Time(1, TimeUnit.YEAR), 1)

        # Division tests: Time divided by Time

    def test_division_by_time(self):
        self.assertEqual(self.day / self.hour, 24)
        self.assertEqual(self.hour / self.minute, 60)
        self.assertEqual(self.minute / self.second, 60)
        self.assertEqual(self.week / self.day, 7)
        self.assertEqual(self.year / self.month, 12)  # Assuming 12 months per year

        # Division tests: Time divided by scalar

    def test_division_by_scalar(self):
        self.assertEqual(self.day / 2, Time(0.5, TimeUnit.DAY))
        self.assertEqual(self.hour / 30, Time(2, TimeUnit.MINUTE))
        self.assertEqual(self.week / 14, Time(0.5, TimeUnit.DAY))



if __name__ == '__main__':
    unittest.main()
