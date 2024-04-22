from decimal import Decimal

d1 = "123.45"
d2 = 123.564778

print(f"{d2:.30f}")
d2 = round(d2,10)
print(type(d1))

print(str(d2))
print(f"{d2:.30f}")
d2 = Decimal.from_float(d2)
print(d2)
print(f"{d2:.30f}")
print(len("1111111111"))