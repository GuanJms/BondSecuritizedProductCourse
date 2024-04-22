from decimal import Decimal

print(f"{0.1:.30f}")
print(f"{0.2:.30f}")

d1 = Decimal("0.1")
d2 = Decimal("0.2")

d1_ = Decimal(0.1)
d2_ = Decimal(0.2)

print(f"{d1:.30f}")
print(f"{d2:.30f}")

print(f"{d1_:.30f}")
print(f"{d2_:.30f}")

d3 = d1 + d2
print(type(d3))
print(f"{d3:.30f}")

print(d3 / 3)
print(type(d3 / 3))

import numpy_financial as npf

npf.pmt(monthly_rate, months, mortgage_amount)
