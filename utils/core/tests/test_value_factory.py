import unittest
from decimal import Decimal
from utils.core import Value, CurrencyType
from utils.core import ValueFactory


class TestValueFactory(unittest.TestCase):
    def test_create_value(self):
        # Test with string
        value = ValueFactory.create_value("123.45", CurrencyType.USD)
        self.assertIsInstance(value, Value)
        self.assertEqual(value.value, Decimal("123.45"))
        self.assertEqual(value.currency, CurrencyType.USD)

        # Test with float
        value = ValueFactory.create_value(123.45, CurrencyType.USD)
        self.assertIsInstance(value, Value)
        self.assertAlmostEquals(value.value, Decimal("123.45"), places=5)
        self.assertEqual(value.currency, CurrencyType.USD)

        # Test with Decimal
        value = ValueFactory.create_value(Decimal("123.45"), CurrencyType.USD)
        self.assertIsInstance(value, Value)
        self.assertEqual(value.value, Decimal("123.45"))
        self.assertEqual(value.currency, CurrencyType.USD)

        # Test with invalid type
        with self.assertRaises(ValueError):
            ValueFactory.create_value([], CurrencyType.USD)


if __name__ == "__main__":
    unittest.main()
